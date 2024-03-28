#!/usr/bin/env python3

from enum import Enum
from io import BytesIO
from pathlib import Path
from pprint import pprint

import typer


# fmt: off
# This got rather duplicative. 
class Constants(Enum):
    CONSTANT_Class              = 7
    CONSTANT_Fieldref           = 9
    CONSTANT_Methodref          = 10
    CONSTANT_InterfaceMethodref = 11
    CONSTANT_String             = 8
    CONSTANT_Integer            = 3
    CONSTANT_Float              = 4
    CONSTANT_Long               = 5
    CONSTANT_Double             = 6
    CONSTANT_NameAndType        = 12
    CONSTANT_Utf8               = 1
    CONSTANT_MethodHandle       = 15
    CONSTANT_MethodType         = 16
    CONSTANT_InvokeDynamic      = 18


ACCESS_FLAGS = {
    "class":  [
        ("ACC_PUBLIC"       ,0x0001),
        ("ACC_FINAL"        ,0x0010),
        ("ACC_SUPER"        ,0x0020),
        ("ACC_INTERFACE"    ,0x0200),
        ("ACC_ABSTRACT"     ,0x0400),
        ("ACC_SYNTHETIC"    ,0x1000),
        ("ACC_ANNOTATION"   ,0x2000),
        ("ACC_ENUM"         ,0x4000),
    ],
    "field": [
        ("ACC_PUBLIC"       ,0x0001),
        ("ACC_PRIVATE"      ,0x0002),
        ("ACC_PROTECTED"    ,0x0004),
        ("ACC_STATIC"       ,0x0008),
        ("ACC_FINAL"        ,0x0010),
        ("ACC_VOLATILE"     ,0x0040),
        ("ACC_TRANSIENT"    ,0x0080),
        ("ACC_SYNTHETIC"    ,0x1000),
        ("ACC_ENUM"         ,0x4000),
    ],
    "method": [
        ("ACC_PUBLIC"       ,0x0001),
        ("ACC_PRIVATE"      ,0x0002),
        ("ACC_PROTECTED"    ,0x0004),
        ("ACC_STATIC"       ,0x0008),
        ("ACC_FINAL"        ,0x0010),
        ("ACC_SYNCHRONIZED" ,0x0020),
        ("ACC_BRIDGE"       ,0x0040),
        ("ACC_VARARGS"      ,0x0080),
        ("ACC_NATIVE"       ,0x0100),
        ("ACC_ABSTRACT"     ,0x0400),
        ("ACC_STRICT"       ,0x0800),
        ("ACC_SYNTHETIC"    ,0x1000),
    ],
}
# fmt: on


def parse_ux(file: BytesIO, length: int) -> int:
    return int.from_bytes(file.read(length), "big")


def parse_u1(file: BytesIO) -> int:
    return parse_ux(file, 1)


def parse_u2(file: BytesIO) -> int:
    return parse_ux(file, 2)


def parse_u4(file: BytesIO) -> int:
    return parse_ux(file, 4)


def parse_constant_pool(f: BytesIO, pool_size: int) -> int:
    constant_pool = []

    # We could map each constant tag to its corresponding processing logic.
    # Would that be better? This looks horrendous.
    for _ in range(pool_size):
        cp_info = {}
        tag = parse_u1(f)
        constant = Constants(tag)

        if constant in (
            Constants.CONSTANT_Methodref,
            Constants.CONSTANT_InterfaceMethodref,
            Constants.CONSTANT_Fieldref,
        ):
            cp_info["tag"] = constant.value
            cp_info["class_index"] = parse_u2(f)
            cp_info["name_and_type_index"] = parse_u2(f)
        elif constant in (Constants.CONSTANT_Class, Constants.CONSTANT_String):
            cp_info["tag"] = constant.value
            cp_info["name_index"] = parse_u2(f)
        elif constant == Constants.CONSTANT_Utf8:
            cp_info["tag"] = constant.value
            cp_info["length"] = parse_u2(f)
            cp_info["bytes"] = f.read(cp_info["length"])
        elif constant == Constants.CONSTANT_NameAndType:
            cp_info["tag"] = constant.value
            cp_info["name_index"] = parse_u2(f)
            cp_info["descriptor_index"] = parse_u2(f)
        elif constant in (Constants.CONSTANT_Integer, Constants.CONSTANT_Float):
            cp_info["tag"] = constant.value
            cp_info["bytes"] = f.read(4)
        elif constant in (Constants.CONSTANT_Long, Constants.CONSTANT_Double):
            cp_info["tag"] = constant.value
            cp_info["high_bytes"] = f.read(4)
            cp_info["low_bytes"] = f.read(4)
        elif constant == Constants.CONSTANT_MethodHandle:
            cp_info["tag"] = constant.value
            cp_info["reference_kind"] = parse_u1(f)
            cp_info["reference_index"] = parse_u2(f)
        elif constant == Constants.CONSTANT_MethodType:
            cp_info["tag"] = constant.value
            cp_info["descriptor_index"] = parse_u2(f)
        elif constant == Constants.CONSTANT_InvokeDynamic:
            cp_info["tag"] = constant.value
            cp_info["bootstrap_method_attr_index"] = parse_u2(f)
            cp_info["name_and_type_index"] = parse_u2(f)
        else:
            assert False, f"Unexpected tag encountered {tag = }"
        constant_pool.append(cp_info)
    return constant_pool


def parse_access_flags(val: int, flags: [(str, int)]) -> list[str]:
    return [name for (name, mask) in flags if not (val & mask)]


def parse_attributes(f: BytesIO, attributes_count: int) -> list:
    attributes = []

    for _ in range(attributes_count):
        attribute_info = {}
        attribute_info["attribute_name_index"] = parse_u2(f)
        attribute_info["attribute_length"] = parse_u4(f)
        attribute_info["info"] = f.read(attribute_info["attribute_length"])
        attributes.append(attribute_info)

    return attributes


def parse_methods(f: BytesIO, methods_count: int) -> list:
    methods = []

    for _ in range(methods_count):
        method_info = {}
        method_info["access_flags"] = parse_access_flags(
            parse_u2(f), ACCESS_FLAGS["method"]
        )
        method_info["name_index"] = parse_u2(f)
        method_info["descriptor_index"] = parse_u2(f)
        method_info["attributes_count"] = parse_u2(f)
        method_info["attributes"] = parse_attributes(f, method_info["attributes_count"])
        methods.append(method_info)
    return methods


def parse_fields(f: BytesIO, fields_count: int) -> dict:
    fields = []

    for _ in range(fields_count):
        field_info = {}
        field_info["access_flags"] = parse_access_flags(
            parse_u2(f), ACCESS_FLAGS["field"]
        )
        field_info["name_index"] = parse_u2(f)
        field_info["descriptor_index"] = parse_u2(f)
        field_info["attributes_count"] = parse_u2(f)
        field_info["attributes"] = parse_attributes(f, field_info["attributes_count"])
        fields.append(field_info)

    return fields


def parse_interfaces(f: BytesIO, interfaces_count: int) -> dict:
    interfaces = []

    for _ in range(interfaces_count):
        parse_u1(f)  # Discard tag
        class_info = {"tag": "CONSTANT_Class", "name_index": parse_u2()}
        interfaces.append(class_info)

    return interfaces


def parse_class_file(f: BytesIO) -> dict:
    class_file = {}
    class_file["magic"] = str(hex(parse_u4(f))).upper()
    class_file["minor"] = parse_u2(f)
    class_file["major"] = parse_u2(f)
    class_file["constant_pool_count"] = parse_u2(f)
    class_file["constant_pool"] = parse_constant_pool(
        f, class_file["constant_pool_count"] - 1
    )
    class_file["access_flags"] = parse_access_flags(parse_u2(f), ACCESS_FLAGS["class"])
    class_file["this_class"] = parse_u2(f)
    class_file["super_class"] = parse_u2(f)
    class_file["interfaces_count"] = parse_u2(f)
    class_file["interfaces"] = parse_interfaces(f, class_file["interfaces_count"])
    class_file["fields_count"] = parse_u2(f)
    class_file["fields"] = parse_fields(f, class_file["fields_count"])
    class_file["methods_count"] = parse_u2(f)
    class_file["methods"] = parse_methods(f, class_file["methods_count"])
    class_file["attributes_count"] = parse_u2(f)
    class_file["attributes"] = parse_attributes(f, class_file["attributes_count"])

    return class_file


def main(file_path: Path) -> None:
    with open(file_path, mode="rb") as f:
        class_file = parse_class_file(BytesIO(f.read()))
        pprint(class_file)


if __name__ == "__main__":
    typer.run(main)
