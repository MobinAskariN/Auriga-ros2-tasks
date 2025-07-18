// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces:msg/Num.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interfaces/msg/num.h"


#ifndef INTERFACES__MSG__DETAIL__NUM__STRUCT_H_
#define INTERFACES__MSG__DETAIL__NUM__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Struct defined in msg/Num in the package interfaces.
typedef struct interfaces__msg__Num
{
  int64_t num;
  bool finished;
} interfaces__msg__Num;

// Struct for a sequence of interfaces__msg__Num.
typedef struct interfaces__msg__Num__Sequence
{
  interfaces__msg__Num * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__msg__Num__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES__MSG__DETAIL__NUM__STRUCT_H_
