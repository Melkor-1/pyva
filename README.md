# pyva

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://https://github.com/Melkor-1/pyva/edit/main/LICENSE)

Parsing Java SE 7 Class File in Python

The [structure](https://docs.oracle.com/javase/specs/jvms/se7/html/jvms-4.html#jvms-4.6) of a class file consists of a single structure (presented here using pseudostructures written in a C-like structure notation):

```java
ClassFile {
    u4             magic;
    u2             minor_version;
    u2             major_version;
    u2             constant_pool_count;
    cp_info        constant_pool[constant_pool_count-1];
    u2             access_flags;
    u2             this_class;
    u2             super_class;
    u2             interfaces_count;
    u2             interfaces[interfaces_count];
    u2             fields_count;
    field_info     fields[fields_count];
    u2             methods_count;
    method_info    methods[methods_count];
    u2             attributes_count;
    attribute_info attributes[attributes_count];
}
```

The script parses the class file into a dictionary (except for the attributes).

For a class file generated for this simple program:
  
```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

the script produces:
```none
{'access_flags': ['ACC_FINAL',
                  'ACC_INTERFACE',
                  'ACC_ABSTRACT',
                  'ACC_SYNTHETIC',
                  'ACC_ANNOTATION',
                  'ACC_ENUM'],
 'attributes': [{'attribute_length': 2,
                 'attribute_name_index': 13,
                 'info': b'\x00\x0e'}],
 'attributes_count': 1,
 'constant_pool': [{'class_index': 6, 'name_and_type_index': 15, 'tag': 10},
                   {'class_index': 16, 'name_and_type_index': 17, 'tag': 9},
                   {'name_index': 18, 'tag': 8},
                   {'class_index': 19, 'name_and_type_index': 20, 'tag': 10},
                   {'name_index': 21, 'tag': 7},
                   {'name_index': 22, 'tag': 7},
                   {'bytes': b'<init>', 'length': 6, 'tag': 1},
                   {'bytes': b'()V', 'length': 3, 'tag': 1},
                   {'bytes': b'Code', 'length': 4, 'tag': 1},
                   {'bytes': b'LineNumberTable', 'length': 15, 'tag': 1},
                   {'bytes': b'main', 'length': 4, 'tag': 1},
                   {'bytes': b'([Ljava/lang/String;)V', 'length': 22, 'tag': 1},
                   {'bytes': b'SourceFile', 'length': 10, 'tag': 1},
                   {'bytes': b'Main.java', 'length': 9, 'tag': 1},
                   {'descriptor_index': 8, 'name_index': 7, 'tag': 12},
                   {'name_index': 23, 'tag': 7},
                   {'descriptor_index': 25, 'name_index': 24, 'tag': 12},
                   {'bytes': b'Hello, World!', 'length': 13, 'tag': 1},
                   {'name_index': 26, 'tag': 7},
                   {'descriptor_index': 28, 'name_index': 27, 'tag': 12},
                   {'bytes': b'Main', 'length': 4, 'tag': 1},
                   {'bytes': b'java/lang/Object', 'length': 16, 'tag': 1},
                   {'bytes': b'java/lang/System', 'length': 16, 'tag': 1},
                   {'bytes': b'out', 'length': 3, 'tag': 1},
                   {'bytes': b'Ljava/io/PrintStream;', 'length': 21, 'tag': 1},
                   {'bytes': b'java/io/PrintStream', 'length': 19, 'tag': 1},
                   {'bytes': b'println', 'length': 7, 'tag': 1},
                   {'bytes': b'(Ljava/lang/String;)V', 'length': 21, 'tag': 1}],
 'constant_pool_count': 29,
 'fields': [],
 'fields_count': 0,
 'interfaces': [],
 'interfaces_count': 0,
 'magic': '0XCAFEBABE',
 'major': 55,
 'methods': [{'access_flags': ['ACC_PRIVATE',
                               'ACC_PROTECTED',
                               'ACC_STATIC',
                               'ACC_FINAL',
                               'ACC_SYNCHRONIZED',
                               'ACC_BRIDGE',
                               'ACC_VARARGS',
                               'ACC_NATIVE',
                               'ACC_ABSTRACT',
                               'ACC_STRICT',
                               'ACC_SYNTHETIC'],
              'attributes': [{'attribute_length': 29,
                              'attribute_name_index': 9,
                              'info': b'\x00\x01\x00\x01\x00\x00\x00\x05'
                                      b'*\xb7\x00\x01\xb1\x00\x00\x00'
                                      b'\x01\x00\n\x00\x00\x00\x06\x00'
                                      b'\x01\x00\x00\x00\x01'}],
              'attributes_count': 1,
              'descriptor_index': 8,
              'name_index': 7},
             {'access_flags': ['ACC_PRIVATE',
                               'ACC_PROTECTED',
                               'ACC_FINAL',
                               'ACC_SYNCHRONIZED',
                               'ACC_BRIDGE',
                               'ACC_VARARGS',
                               'ACC_NATIVE',
                               'ACC_ABSTRACT',
                               'ACC_STRICT',
                               'ACC_SYNTHETIC'],
              'attributes': [{'attribute_length': 37,
                              'attribute_name_index': 9,
                              'info': b'\x00\x02\x00\x01\x00\x00\x00\t'
                                      b'\xb2\x00\x02\x12\x03\xb6\x00\x04'
                                      b'\xb1\x00\x00\x00\x01\x00\n\x00'
                                      b'\x00\x00\n\x00\x02\x00\x00\x00'
                                      b'\x03\x00\x08\x00\x04'}],
              'attributes_count': 1,
              'descriptor_index': 12,
              'name_index': 11}],
 'methods_count': 2,
 'minor': 0,
 'super_class': 6,
 'this_class': 5}
```
