/**
 * ============================================================================
 *   __  __           _     ____             ____                       _
 *  |  \/  |         (_)   |  _ \           / ___|  ___ _ ____   ____ _ ___
 *  | |\/| |  __ _  _  _  | |_) |  _____  | |  _  / _ \ \ /\ / / _` / __|
 *  | |  | | / _` || | | |  _ <  |_____| | |_| |  __/ \ V  V / (_| \__ \
 *  |_|  |_|| (_| || |_| | |_) |         \____| \___|  \_/\_/ \__,_|___/
 *
 *  NumC - NumPy-like Library for C / NumPy风格的C语言数组计算库
 *
 *  Version: 1.0.0
 *  License: GPLv3
 *
 *  Homepage: https://github.com/cycleuser/NumC
 *
 *  ============================================================================
 *
 *  使用说明 / Usage:
 *
 *  1. 单文件使用 (Single file usage):
 *     #define NC_IMPLEMENTATION
 *     #include "../NumC.h"
 *
 *  2. 编译 (Compile):
 *     gcc -o program program.c -lm
 *
 *  ============================================================================
 *
 *  示例 / Examples:
 *
 *  示例1: 基本数组创建和运算
 *  Example 1: Basic array creation and operations
 *
 *      #define NC_IMPLEMENTATION
 *      #include "../NumC.h"
 *      #include <stdio.h>
 *
 *      int main() {
 *          NCArray *a = NC_INT(1, 2, 3, 4, 5);      // [1, 2, 3, 4, 5]
 *          NCArray *b = NC_FLOAT(1.0, 2.0, 3.0);     // [1.0, 2.0, 3.0]
 *          NCArray *sum = nc_add(a, a);
 *          NCArray *prod = nc_multiply(a, b);
 *          nc_print(sum);  // [2, 4, 6, 8, 10]
 *          nc_print(prod); // [1, 4, 9, 16, 25]
 *          nc_release(a); nc_release(b); nc_release(sum); nc_release(prod);
 *          return 0;
 *      }
 *
 *  示例2: 2D数组和矩阵运算
 *  Example 2: 2D arrays and matrix operations
 *
 *      NCArray *A = NC_INT2D(2, 3, 1, 2, 3, 4, 5, 6);  // [[1,2,3],[4,5,6]]
 *      NCArray *B = NC_FLOAT2D(2, 3, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0); // identity-like
 *      NCArray *C = nc_matmul(A, nc_transpose(A, NULL)); // A @ A.T
 *      NCArray *trace = nc_trace(C, 0, 0, 1);
 *      nc_print(C);
 *      nc_release(A); nc_release(B); nc_release(C); nc_release(trace);
 *
 *  示例3: 数学函数
 *  Example 3: Mathematical functions
 *
 *      NCArray *x = NC_FLOAT(0, M_PI/4, M_PI/2, M_PI); // [0, pi/4, pi/2, pi]
 *      NCArray *sin_x = nc_sin(x);
 *      NCArray *cos_x = nc_cos(x);
 *      NCArray *exp_x = nc_exp(x);
 *      NCArray *sqrt_x = nc_sqrt(x);
 *      nc_print(sin_x); nc_print(cos_x); nc_print(exp_x); nc_print(sqrt_x);
 *      nc_release(x); nc_release(sin_x); nc_release(cos_x);
 *      nc_release(exp_x); nc_release(sqrt_x);
 *
 *  示例4: 归约操作
 *  Example 4: Reduction operations
 *
 *      NCArray *arr = NC_INT(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
 *      NCArray *sum = nc_sum(arr, NULL, 0);    // 55
 *      NCArray *mean = nc_mean(arr, NULL, 0); // 5.5
 *      NCArray *min = nc_min(arr, NULL, 0);   // 1
 *      NCArray *max = nc_max(arr, NULL, 0);  // 10
 *      NCArray *std = nc_std(arr, NULL, 0);  // ~3.03
 *      printf("Sum: %.0f, Mean: %.1f, Min: %.0f, Max: %.0f, Std: %.2f\n",
 *             ((double*)sum->data)[0], ((double*)mean->data)[0],
 *             ((double*)min->data)[0], ((double*)max->data)[0],
 *             ((double*)std->data)[0]);
 *      nc_release(arr); nc_release(sum); nc_release(mean);
 *      nc_release(min); nc_release(max); nc_release(std);
 *
 *  示例5: 随机数和统计
 *  Example 5: Random numbers and statistics
 *
 *      nc_random_seed(42);  // 固定种子以便复现
 *      NCArray *uniform = nc_random_rand(2, (int64_t[]){3, 4}); // 均匀分布 [0,1)
 *      NCArray *normal = nc_random_randn(2, (int64_t[]){3, 4}, NC_FLOAT64); // 正态分布
 *      NCArray *integers = nc_random_randint(0, 100, 2, (int64_t[]){3, 4}); // [0,100) 整数
 *      nc_print(uniform); nc_print(normal); nc_print(integers);
 *      nc_random_shuffle(uniform);
 *      nc_print(uniform); // 现在是随机排列的
 *      nc_release(uniform); nc_release(normal); nc_release(integers);
 *
 *  示例6: 数组操作
 *  Example 6: Array operations
 *
 *      NCArray *a = NC_INT(1, 2, 3, 4, 5, 6);
 *      NCArray *reshaped = nc_reshape(nc_copy(a), 2, (int64_t[]){2, 3}); // [[1,2,3],[4,5,6]]
 *      NCArray *flat = ncflatten(reshaped); // [1,2,3,4,5,6]
 *      NCArray *trans = nctranspose(reshaped, NULL); // [[1,4],[2,5],[3,6]]
 *      NCArray *arrs[2] = {NC_INT(1,2,3), NC_INT(4,5,6)};
 *      NCArray *concat = nc_concatenate(arrs, 2, 0); // [1,2,3,4,5,6]
 *      NCArray *stacked = nc_stack(arrs, 2, 0); // [[1,2,3],[4,5,6]]
 *      nc_print(reshaped); nc_print(flat); nc_print(trans); nc_print(concat);
 *      nc_release(a); nc_release(reshaped); nc_release(flat);
 *      nc_release(trans); nc_release(concat); nc_release(stacked);
 *      nc_release(arrs[0]); nc_release(arrs[1]);
 *
 *  示例7: 比较和逻辑运算
 *  Example 7: Comparison and logical operations
 *
 *      NCArray *a = NC_INT(1, 2, 3, 4, 5);
 *      NCArray *b = NC_INT(5, 4, 3, 2, 1);
 *      NCArray *eq = nc_equal(a, b);  // [false, false, true, false, false]
 *      NCArray *gt = nc_greater(a, b); // [false, false, false, true, true]
 *      NCArray *and_result = nc_logical_and(eq, gt); // [false, false, false, false, false]
 *      NCArray *not_a = nc_logical_not(eq); // [true, true, false, true, true]
 *      nc_print(eq); nc_print(gt); nc_print(and_result); nc_print(not_a);
 *      nc_release(a); nc_release(b); nc_release(eq); nc_release(gt);
 *      nc_release(and_result); nc_release(not_a);
 *
 *  示例8: 保存和加载
 *  Example 8: Save and load
 *
 *      NCArray *data = NC_FLOAT(1.0, 2.0, 3.0, 4.0, 5.0);
 *      nc_save("data.bin", data);  // 保存到文件
 *      NCArray *loaded = nc_load("data.bin");  // 从文件加载
 *      nc_print(loaded);
 *      nc_release(data); nc_release(loaded);
 *
 *  ============================================================================
 */

#ifndef NUMC_H
#define NUMC_H

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>
#include <stdarg.h>
#include <float.h>

#ifdef __cplusplus
extern "C" {
#endif

#define NC_VERSION "1.0.0"
#define NC_MAX_DIMS 16
#define NC_MAX_TENSOR_SIZE 2147483647

typedef enum {
    NC_OK = 0,
    NC_ERROR = -1,
    NC_MEMORY_ERROR = -2,
    NC_DIMENSION_ERROR = -3,
    NC_SHAPE_ERROR = -4,
    NC_TYPE_ERROR = -5,
    NC_VALUE_ERROR = -6,
    NC_INDEX_ERROR = -7,
    NC_NOT_IMPLEMENTED = -8
} NCStatus;

typedef enum {
    NC_INVALID = 0,
    NC_BOOL,
    NC_INT8, NC_INT16, NC_INT32, NC_INT64,
    NC_UINT8, NC_UINT16, NC_UINT32, NC_UINT64,
    NC_FLOAT32, NC_FLOAT64,
    NC_COMPLEX64, NC_COMPLEX128
} NCDataType;

typedef struct NCArray {
    void *data;
    int32_t ndim;
    int64_t shape[NC_MAX_DIMS];
    int64_t strides[NC_MAX_DIMS];
    size_t itemsize;
    NCDataType dtype;
    bool owns_data;
    int refcount;
    struct NCArray *base;
} NCArray;

typedef struct NCComplex64 { float real, imag; } NCComplex64;
typedef struct NCComplex128 { double real, imag; } NCComplex128;

const char *nc_version(void);
const char *nc_status_string(NCStatus status);
size_t nc_dtype_size(NCDataType dtype);
const char *nc_dtype_name(NCDataType dtype);
NCDataType nc_dtype_from_string(const char *name);
bool nc_dtype_is_integer(NCDataType dtype);
bool nc_dtype_is_float(NCDataType dtype);
bool nc_dtype_is_numeric(NCDataType dtype);

size_t nc_size(NCArray *arr);
size_t nc_nbytes(NCArray *arr);
int32_t nc_ndim(NCArray *arr);
int64_t *nc_shape(NCArray *arr);
int64_t nc_shape_at(NCArray *arr, int32_t dim);
int64_t *nc_strides(NCArray *arr);
size_t nc_itemsize(NCArray *arr);
NCDataType nc_dtype(NCArray *arr);
bool nc_is_contiguous(NCArray *arr);
void nc_update_strides(NCArray *arr);

NCArray *nc_empty(int32_t ndim, const int64_t *shape, NCDataType dtype);
NCArray *nc_zeros(int32_t ndim, const int64_t *shape, NCDataType dtype);
NCArray *nc_ones(int32_t ndim, const int64_t *shape, NCDataType dtype);
NCArray *nc_full(int32_t ndim, const int64_t *shape, void *fill_value, NCDataType dtype);
NCArray *nc_arange(double start, double stop, double step, NCDataType dtype);
NCArray *nc_linspace(double start, double stop, int64_t num, bool endpoint, NCDataType dtype);
NCArray *nc_identity(int64_t n, NCDataType dtype);
NCArray *nc_eye(int64_t n, int64_t m, int64_t k, NCDataType dtype);
NCArray *nc_diag(NCArray *arr, int64_t k);
NCArray *nc_copy(NCArray *arr);

NCStatus nc_reshape(NCArray *arr, int32_t ndim, const int64_t *shape);
NCArray *nctranspose(NCArray *arr, const int32_t *axes);
NCArray *ncflatten(NCArray *arr);

NCArray *nc_add(NCArray *a, NCArray *b);
NCArray *nc_subtract(NCArray *a, NCArray *b);
NCArray *nc_multiply(NCArray *a, NCArray *b);
NCArray *nc_divide(NCArray *a, NCArray *b);
NCArray *nc_power(NCArray *a, NCArray *b);
NCArray *nc_mod(NCArray *a, NCArray *b);
NCArray *nc_equal(NCArray *a, NCArray *b);
NCArray *nc_not_equal(NCArray *a, NCArray *b);
NCArray *nc_less(NCArray *a, NCArray *b);
NCArray *nc_greater(NCArray *a, NCArray *b);
NCArray *nc_less_equal(NCArray *a, NCArray *b);
NCArray *nc_greater_equal(NCArray *a, NCArray *b);
NCArray *nc_logical_and(NCArray *a, NCArray *b);
NCArray *nc_logical_or(NCArray *a, NCArray *b);
NCArray *nc_logical_not(NCArray *a);

NCArray *nc_abs(NCArray *arr);
NCArray *nc_sign(NCArray *arr);
NCArray *nc_floor(NCArray *arr);
NCArray *nc_ceil(NCArray *arr);
NCArray *nc_round(NCArray *arr);
NCArray *nc_exp(NCArray *arr);
NCArray *nc_log(NCArray *arr);
NCArray *nc_log10(NCArray *arr);
NCArray *nc_sqrt(NCArray *arr);
NCArray *nc_sin(NCArray *arr);
NCArray *nc_cos(NCArray *arr);
NCArray *nc_tan(NCArray *arr);
NCArray *nc_arcsin(NCArray *arr);
NCArray *nc_arccos(NCArray *arr);
NCArray *nc_arctan(NCArray *arr);
NCArray *nc_negate(NCArray *arr);

NCArray *nc_dot(NCArray *a, NCArray *b);
NCArray *nc_matmul(NCArray *a, NCArray *b);
NCArray *nc_inner(NCArray *a, NCArray *b);
NCArray *nc_outer(NCArray *a, NCArray *b);
NCArray *nc_cross(NCArray *a, NCArray *b, int32_t axis);
NCArray *nc_trace(NCArray *arr, int32_t offset, int32_t axis1, int32_t axis2);

NCArray *nc_sum(NCArray *arr, const int32_t *axis, int32_t naxis);
NCArray *nc_prod(NCArray *arr, const int32_t *axis, int32_t naxis);
NCArray *nc_mean(NCArray *arr, const int32_t *axis, int32_t naxis);
NCArray *nc_var(NCArray *arr, const int32_t *axis, int32_t naxis);
NCArray *nc_std(NCArray *arr, const int32_t *axis, int32_t naxis);
NCArray *nc_min(NCArray *arr, const int32_t *axis, int32_t naxis);
NCArray *nc_max(NCArray *arr, const int32_t *axis, int32_t naxis);
NCArray *nc_argmin(NCArray *arr, int32_t axis);
NCArray *nc_argmax(NCArray *arr, int32_t axis);
NCArray *nc_all(NCArray *arr, const int32_t *axis, int32_t naxis);
NCArray *nc_any(NCArray *arr, const int32_t *axis, int32_t naxis);
NCArray *nc_cumsum(NCArray *arr, int32_t axis);

int64_t nc_count_nonzero(NCArray *arr);
bool nc_isnan(NCArray *arr);
bool nc_isfinite(NCArray *arr);

NCArray *nc_concatenate(NCArray **arrays, int32_t n, int32_t axis);
NCArray *nc_stack(NCArray **arrays, int32_t n, int32_t axis);

NCArray *nc_random_rand(int32_t ndim, const int64_t *shape);
NCArray *nc_random_randn(int32_t ndim, const int64_t *shape, NCDataType dtype);
NCArray *nc_random_randint(int64_t low, int64_t high, int32_t ndim, const int64_t *shape);
void nc_random_seed(uint64_t seed);
void nc_random_shuffle(NCArray *arr);

NCArray *nc_linalg_norm(NCArray *arr, const char *ord);

void nc_print(NCArray *arr);
void nc_release(NCArray *arr);
NCArray *nc_retain(NCArray *arr);
NCStatus nc_save(const char *filename, NCArray *arr);
NCArray *nc_load(const char *filename);

#define nc_free(arr) nc_release(arr)

NCArray *nc_make_1d(NCDataType dtype, int64_t n, ...);
NCArray *nc_make_2d(NCDataType dtype, int64_t rows, int64_t cols, ...);
NCArray *nc_make_1d_auto(int n, ...);
NCArray *nc_make_2d_auto(int64_t rows, int64_t cols, int n, ...);
NCArray *nc_make_1d_float_auto(int n, ...);
NCArray *nc_make_2d_float_auto(int64_t rows, int64_t cols, int n, ...);

#define _NC_COUNT_ARGS(...) _NC_COUNT_ARGS_IMPL(__VA_ARGS__, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)
#define _NC_COUNT_ARGS_IMPL(_1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14, _15, _16, _N, ...) _N

#define NC_INT(...) nc_make_1d_auto(_NC_COUNT_ARGS(__VA_ARGS__), (int64_t)__VA_ARGS__)
#define NC_FLOAT(...) nc_make_1d_float_auto(_NC_COUNT_ARGS(__VA_ARGS__), (double)__VA_ARGS__)
#define NC_INT2D(_rows, _cols, ...) nc_make_2d_auto(_rows, _cols, _NC_COUNT_ARGS(__VA_ARGS__), (int64_t)__VA_ARGS__)
#define NC_FLOAT2D(_rows, _cols, ...) nc_make_2d_float_auto(_rows, _cols, _NC_COUNT_ARGS(__VA_ARGS__), (double)__VA_ARGS__)

#define NC_BOOL(...) nc_make_1d(NC_BOOL, _NC_COUNT_ARGS(__VA_ARGS__), (int64_t)__VA_ARGS__)
#define NC_INT8(...) nc_make_1d(NC_INT8, _NC_COUNT_ARGS(__VA_ARGS__), (int64_t)__VA_ARGS__)
#define NC_INT16(...) nc_make_1d(NC_INT16, _NC_COUNT_ARGS(__VA_ARGS__), (int64_t)__VA_ARGS__)
#define NC_INT32(...) nc_make_1d(NC_INT32, _NC_COUNT_ARGS(__VA_ARGS__), (int64_t)__VA_ARGS__)
#define NC_INT64(...) nc_make_1d(NC_INT64, _NC_COUNT_ARGS(__VA_ARGS__), (int64_t)__VA_ARGS__)
#define NC_UINT8(...) nc_make_1d(NC_UINT8, _NC_COUNT_ARGS(__VA_ARGS__), (int64_t)__VA_ARGS__)
#define NC_UINT16(...) nc_make_1d(NC_UINT16, _NC_COUNT_ARGS(__VA_ARGS__), (int64_t)__VA_ARGS__)
#define NC_UINT32(...) nc_make_1d(NC_UINT32, _NC_COUNT_ARGS(__VA_ARGS__), (int64_t)__VA_ARGS__)
#define NC_UINT64(...) nc_make_1d(NC_UINT64, _NC_COUNT_ARGS(__VA_ARGS__), (int64_t)__VA_ARGS__)
#define NC_FLOAT32(...) nc_make_1d(NC_FLOAT32, _NC_COUNT_ARGS(__VA_ARGS__), (double)__VA_ARGS__)
#define NC_FLOAT64(...) nc_make_1d(NC_FLOAT64, _NC_COUNT_ARGS(__VA_ARGS__), (double)__VA_ARGS__)

#ifdef __cplusplus
}
#endif

#endif

#ifdef NC_IMPLEMENTATION

#include <string.h>
#include <stdio.h>

const char *nc_version(void) { return NC_VERSION; }

const char *nc_status_string(NCStatus status) {
    switch (status) {
        case NC_OK: return "No error";
        case NC_ERROR: return "Generic error";
        case NC_MEMORY_ERROR: return "Memory allocation failed";
        case NC_DIMENSION_ERROR: return "Dimension mismatch";
        case NC_SHAPE_ERROR: return "Shape mismatch";
        case NC_TYPE_ERROR: return "Type mismatch";
        case NC_VALUE_ERROR: return "Value error";
        case NC_INDEX_ERROR: return "Index error";
        case NC_NOT_IMPLEMENTED: return "Not implemented";
        default: return "Unknown error";
    }
}

size_t nc_dtype_size(NCDataType dtype) {
    switch (dtype) {
        case NC_BOOL: return sizeof(bool);
        case NC_INT8: return sizeof(int8_t);
        case NC_INT16: return sizeof(int16_t);
        case NC_INT32: return sizeof(int32_t);
        case NC_INT64: return sizeof(int64_t);
        case NC_UINT8: return sizeof(uint8_t);
        case NC_UINT16: return sizeof(uint16_t);
        case NC_UINT32: return sizeof(uint32_t);
        case NC_UINT64: return sizeof(uint64_t);
        case NC_FLOAT32: return sizeof(float);
        case NC_FLOAT64: return sizeof(double);
        case NC_COMPLEX64: return sizeof(NCComplex64);
        case NC_COMPLEX128: return sizeof(NCComplex128);
        default: return 0;
    }
}

const char *nc_dtype_name(NCDataType dtype) {
    switch (dtype) {
        case NC_BOOL: return "bool";
        case NC_INT8: return "int8";
        case NC_INT16: return "int16";
        case NC_INT32: return "int32";
        case NC_INT64: return "int64";
        case NC_UINT8: return "uint8";
        case NC_UINT16: return "uint16";
        case NC_UINT32: return "uint32";
        case NC_UINT64: return "uint64";
        case NC_FLOAT32: return "float32";
        case NC_FLOAT64: return "float64";
        case NC_COMPLEX64: return "complex64";
        case NC_COMPLEX128: return "complex128";
        default: return "unknown";
    }
}

NCDataType nc_dtype_from_string(const char *name) {
    if (strcmp(name, "bool") == 0) return NC_BOOL;
    if (strcmp(name, "int8") == 0) return NC_INT8;
    if (strcmp(name, "int16") == 0) return NC_INT16;
    if (strcmp(name, "int32") == 0) return NC_INT32;
    if (strcmp(name, "int64") == 0) return NC_INT64;
    if (strcmp(name, "uint8") == 0) return NC_UINT8;
    if (strcmp(name, "uint16") == 0) return NC_UINT16;
    if (strcmp(name, "uint32") == 0) return NC_UINT32;
    if (strcmp(name, "uint64") == 0) return NC_UINT64;
    if (strcmp(name, "float32") == 0) return NC_FLOAT32;
    if (strcmp(name, "float64") == 0) return NC_FLOAT64;
    if (strcmp(name, "complex64") == 0) return NC_COMPLEX64;
    if (strcmp(name, "complex128") == 0) return NC_COMPLEX128;
    return NC_INVALID;
}

bool nc_dtype_is_integer(NCDataType dtype) { return dtype >= NC_BOOL && dtype <= NC_UINT64; }
bool nc_dtype_is_float(NCDataType dtype) { return dtype == NC_FLOAT32 || dtype == NC_FLOAT64; }
bool nc_dtype_is_numeric(NCDataType dtype) { return nc_dtype_is_integer(dtype) || nc_dtype_is_float(dtype); }

size_t nc_size(NCArray *arr) {
    if (!arr) return 0;
    size_t size = 1;
    for (int32_t i = 0; i < arr->ndim; i++) size *= arr->shape[i];
    return size;
}

size_t nc_nbytes(NCArray *arr) { return nc_size(arr) * arr->itemsize; }
int32_t nc_ndim(NCArray *arr) { return arr ? arr->ndim : 0; }
int64_t *nc_shape(NCArray *arr) { return arr ? arr->shape : NULL; }
int64_t nc_shape_at(NCArray *arr, int32_t dim) { return (arr && dim >= 0 && dim < arr->ndim) ? arr->shape[dim] : 0; }
int64_t *nc_strides(NCArray *arr) { return arr ? arr->strides : NULL; }
size_t nc_itemsize(NCArray *arr) { return arr ? arr->itemsize : 0; }
NCDataType nc_dtype(NCArray *arr) { return arr ? arr->dtype : NC_INVALID; }

void nc_update_strides(NCArray *arr) {
    if (!arr || arr->ndim == 0) return;
    arr->strides[arr->ndim - 1] = 1;
    for (int32_t i = arr->ndim - 2; i >= 0; i--) arr->strides[i] = arr->strides[i + 1] * arr->shape[i + 1];
}

bool nc_is_contiguous(NCArray *arr) {
    if (!arr) return false;
    int64_t expected_stride = 1;
    for (int32_t i = arr->ndim - 1; i >= 0; i--) {
        if (arr->shape[i] == 1) continue;
        if (arr->strides[i] != expected_stride) return false;
        expected_stride *= arr->shape[i];
    }
    return true;
}

static NCArray *nc_array_create(void *data, int32_t ndim, const int64_t *shape, NCDataType dtype, bool owns_data) {
    if ((!shape && ndim > 0) || ndim < 0 || ndim > NC_MAX_DIMS) return NULL;
    NCArray *arr = (NCArray *)calloc(1, sizeof(NCArray));
    if (!arr) return NULL;
    arr->ndim = ndim;
    arr->dtype = dtype;
    arr->itemsize = nc_dtype_size(dtype);
    arr->owns_data = owns_data;
    arr->refcount = 1;
    arr->base = NULL;
    for (int32_t i = 0; i < ndim; i++) arr->shape[i] = shape[i];
    size_t total_size = 1;
    for (int32_t i = 0; i < ndim; i++) total_size *= shape[i];
    if (data) arr->data = data;
    else if (owns_data) {
        arr->data = calloc(total_size, arr->itemsize);
        if (!arr->data) { free(arr); return NULL; }
    }
    nc_update_strides(arr);
    return arr;
}

NCArray *nc_empty(int32_t ndim, const int64_t *shape, NCDataType dtype) { return nc_array_create(NULL, ndim, shape, dtype, true); }

NCArray *nc_zeros(int32_t ndim, const int64_t *shape, NCDataType dtype) {
    NCArray *arr = nc_empty(ndim, shape, dtype);
    if (arr && arr->data) memset(arr->data, 0, nc_nbytes(arr));
    return arr;
}

NCArray *nc_ones(int32_t ndim, const int64_t *shape, NCDataType dtype) {
    NCArray *arr = nc_empty(ndim, shape, dtype);
    if (!arr) return NULL;
    size_t total = nc_size(arr);
    char *ptr = (char *)arr->data;
    for (size_t i = 0; i < total; i++) {
        switch (dtype) {
            case NC_BOOL: ((bool*)ptr)[i] = 1; break;
            case NC_INT8: ((int8_t*)ptr)[i] = 1; break;
            case NC_INT16: ((int16_t*)ptr)[i] = 1; break;
            case NC_INT32: ((int32_t*)ptr)[i] = 1; break;
            case NC_INT64: ((int64_t*)ptr)[i] = 1; break;
            case NC_UINT8: ((uint8_t*)ptr)[i] = 1; break;
            case NC_UINT16: ((uint16_t*)ptr)[i] = 1; break;
            case NC_UINT32: ((uint32_t*)ptr)[i] = 1; break;
            case NC_UINT64: ((uint64_t*)ptr)[i] = 1; break;
            case NC_FLOAT32: ((float*)ptr)[i] = 1.0f; break;
            case NC_FLOAT64: ((double*)ptr)[i] = 1.0; break;
            default: break;
        }
    }
    return arr;
}

NCArray *nc_full(int32_t ndim, const int64_t *shape, void *fill_value, NCDataType dtype) {
    NCArray *arr = nc_empty(ndim, shape, dtype);
    if (!arr) return NULL;
    size_t total = nc_size(arr);
    size_t esize = arr->itemsize;
    char *ptr = (char *)arr->data;
    for (size_t i = 0; i < total; i++) memcpy(ptr + i * esize, fill_value, esize);
    return arr;
}

NCArray *nc_arange(double start, double stop, double step, NCDataType dtype) {
    if (step == 0) return NULL;
    int64_t n = (int64_t)ceil((stop - start) / step);
    if (n < 0) n = 0;
    int64_t shape[1] = {n};
    NCArray *arr = nc_empty(1, shape, dtype);
    if (!arr) return NULL;
    char *ptr = (char *)arr->data;
    for (int64_t i = 0; i < n; i++) {
        double value = start + i * step;
        switch (dtype) {
            case NC_BOOL: ((bool*)ptr)[i] = (bool)value; break;
            case NC_INT8: ((int8_t*)ptr)[i] = (int8_t)value; break;
            case NC_INT16: ((int16_t*)ptr)[i] = (int16_t)value; break;
            case NC_INT32: ((int32_t*)ptr)[i] = (int32_t)value; break;
            case NC_INT64: ((int64_t*)ptr)[i] = (int64_t)value; break;
            case NC_UINT8: ((uint8_t*)ptr)[i] = (uint8_t)value; break;
            case NC_UINT16: ((uint16_t*)ptr)[i] = (uint16_t)value; break;
            case NC_UINT32: ((uint32_t*)ptr)[i] = (uint32_t)value; break;
            case NC_UINT64: ((uint64_t*)ptr)[i] = (uint64_t)value; break;
            case NC_FLOAT32: ((float*)ptr)[i] = (float)value; break;
            case NC_FLOAT64: ((double*)ptr)[i] = value; break;
            default: break;
        }
    }
    return arr;
}

NCArray *nc_linspace(double start, double stop, int64_t num, bool endpoint, NCDataType dtype) {
    if (num <= 0) return nc_empty(1, (int64_t[]){0}, dtype);
    if (num == 1) {
        NCArray *arr = nc_empty(1, (int64_t[]){1}, dtype);
        if (!arr) return NULL;
        if (dtype == NC_FLOAT32) ((float*)arr->data)[0] = (float)start;
        else if (dtype == NC_FLOAT64) ((double*)arr->data)[0] = start;
        else ((double*)arr->data)[0] = start;
        return arr;
    }
    int64_t n = endpoint ? num : num - 1;
    double step = (stop - start) / n;
    int64_t shape[1] = {num};
    NCArray *arr = nc_empty(1, shape, dtype);
    if (!arr) return NULL;
    char *ptr = (char *)arr->data;
    for (int64_t i = 0; i < num; i++) {
        double value = start + i * step;
        switch (dtype) {
            case NC_BOOL: ((bool*)ptr)[i] = (bool)value; break;
            case NC_INT8: ((int8_t*)ptr)[i] = (int8_t)value; break;
            case NC_INT16: ((int16_t*)ptr)[i] = (int16_t)value; break;
            case NC_INT32: ((int32_t*)ptr)[i] = (int32_t)value; break;
            case NC_INT64: ((int64_t*)ptr)[i] = (int64_t)value; break;
            case NC_UINT8: ((uint8_t*)ptr)[i] = (uint8_t)value; break;
            case NC_UINT16: ((uint16_t*)ptr)[i] = (uint16_t)value; break;
            case NC_UINT32: ((uint32_t*)ptr)[i] = (uint32_t)value; break;
            case NC_UINT64: ((uint64_t*)ptr)[i] = (uint64_t)value; break;
            case NC_FLOAT32: ((float*)ptr)[i] = (float)value; break;
            case NC_FLOAT64: ((double*)ptr)[i] = value; break;
            default: ((double*)ptr)[i] = value; break;
        }
    }
    return arr;
}

NCArray *nc_identity(int64_t n, NCDataType dtype) {
    int64_t shape[2] = {n, n};
    NCArray *arr = nc_zeros(2, shape, dtype);
    if (!arr) return NULL;
    char *ptr = (char *)arr->data;
    for (int64_t i = 0; i < n; i++) {
        size_t idx = i * n + i;
        switch (dtype) {
            case NC_BOOL: ((bool*)ptr)[idx] = true; break;
            case NC_INT8: ((int8_t*)ptr)[idx] = 1; break;
            case NC_INT16: ((int16_t*)ptr)[idx] = 1; break;
            case NC_INT32: ((int32_t*)ptr)[idx] = 1; break;
            case NC_INT64: ((int64_t*)ptr)[idx] = 1; break;
            case NC_UINT8: ((uint8_t*)ptr)[idx] = 1; break;
            case NC_UINT16: ((uint16_t*)ptr)[idx] = 1; break;
            case NC_UINT32: ((uint32_t*)ptr)[idx] = 1; break;
            case NC_UINT64: ((uint64_t*)ptr)[idx] = 1; break;
            case NC_FLOAT32: ((float*)ptr)[idx] = 1.0f; break;
            case NC_FLOAT64: ((double*)ptr)[idx] = 1.0; break;
            default: break;
        }
    }
    return arr;
}

NCArray *nc_eye(int64_t n, int64_t m, int64_t k, NCDataType dtype) {
    int64_t shape[2] = {n, m};
    NCArray *arr = nc_zeros(2, shape, dtype);
    if (!arr) return NULL;
    char *ptr = (char *)arr->data;
    int64_t max_diag = (n < m) ? n : m;
    int64_t start = (k >= 0) ? 0 : -k;
    int64_t end = (k >= 0) ? (max_diag - k) : max_diag;
    for (int64_t i = start; i < end && i < n && (i + k) < m; i++) {
        size_t idx = i * m + (i + k);
        switch (dtype) {
            case NC_BOOL: ((bool*)ptr)[idx] = true; break;
            case NC_INT8: ((int8_t*)ptr)[idx] = 1; break;
            case NC_INT16: ((int16_t*)ptr)[idx] = 1; break;
            case NC_INT32: ((int32_t*)ptr)[idx] = 1; break;
            case NC_INT64: ((int64_t*)ptr)[idx] = 1; break;
            case NC_UINT8: ((uint8_t*)ptr)[idx] = 1; break;
            case NC_UINT16: ((uint16_t*)ptr)[idx] = 1; break;
            case NC_UINT32: ((uint32_t*)ptr)[idx] = 1; break;
            case NC_UINT64: ((uint64_t*)ptr)[idx] = 1; break;
            case NC_FLOAT32: ((float*)ptr)[idx] = 1.0f; break;
            case NC_FLOAT64: ((double*)ptr)[idx] = 1.0; break;
            default: break;
        }
    }
    return arr;
}

NCArray *nc_diag(NCArray *arr, int64_t k) {
    if (!arr) return NULL;
    if (arr->ndim == 1) {
        int64_t n = arr->shape[0] + llabs(k);
        int64_t shape[2] = {n, n};
        NCArray *result = nc_zeros(2, shape, arr->dtype);
        if (!result) return NULL;
        char *rptr = (char *)result->data;
        char *aptr = (char *)arr->data;
        size_t esize = arr->itemsize;
        for (int64_t i = 0; i < arr->shape[0]; i++) {
            int64_t row = (k >= 0) ? i : i - k;
            int64_t col = (k >= 0) ? i + k : i;
            if (row >= 0 && row < n && col >= 0 && col < n)
                memcpy(rptr + (row * n + col) * esize, aptr + i * esize, esize);
        }
        return result;
    }
    return NULL;
}

NCArray *nc_copy(NCArray *arr) {
    if (!arr) return NULL;
    NCArray *result = nc_empty(arr->ndim, arr->shape, arr->dtype);
    if (!result) return NULL;
    memcpy(result->data, arr->data, nc_nbytes(arr));
    return result;
}

NCStatus nc_reshape(NCArray *arr, int32_t ndim, const int64_t *shape) {
    if (!arr || !shape) return NC_ERROR;
    size_t total = nc_size(arr), new_total = 1;
    for (int32_t i = 0; i < ndim; i++) new_total *= shape[i];
    if (total != new_total) return NC_SHAPE_ERROR;
    arr->ndim = ndim;
    for (int32_t i = 0; i < ndim; i++) arr->shape[i] = shape[i];
    nc_update_strides(arr);
    return NC_OK;
}

NCArray *nctranspose(NCArray *arr, const int32_t *axes) {
    if (!arr) return NULL;
    NCArray *result = nc_empty(arr->ndim, arr->shape, arr->dtype);
    if (!result) return NULL;
    if (axes) {
        for (int32_t i = 0; i < arr->ndim; i++) {
            result->shape[i] = arr->shape[axes[i]];
            result->strides[i] = arr->strides[axes[i]];
        }
    } else {
        for (int32_t i = 0; i < arr->ndim; i++) {
            result->shape[i] = arr->shape[arr->ndim - 1 - i];
            result->strides[i] = arr->strides[arr->ndim - 1 - i];
        }
    }
    result->data = arr->data;
    result->owns_data = false;
    result->base = arr;
    arr->refcount++;
    return result;
}

NCArray *ncflatten(NCArray *arr) {
    if (!arr) return NULL;
    int64_t shape[1] = {nc_size(arr)};
    NCArray *result = nc_copy(arr);
    if (!result) return NULL;
    nc_reshape(result, 1, shape);
    return result;
}

static double nc_get_value_as_double(NCArray *arr, size_t linear_idx) {
    char *data = (char *)arr->data;
    int64_t idx = 0, temp = linear_idx;
    for (int32_t d = arr->ndim - 1; d >= 0; d--) {
        idx += (temp % arr->shape[d]) * arr->strides[d];
        temp /= arr->shape[d];
    }
    switch (arr->dtype) {
        case NC_BOOL: return ((bool*)data)[idx] ? 1.0 : 0.0;
        case NC_INT8: return (double)((int8_t*)data)[idx];
        case NC_INT16: return (double)((int16_t*)data)[idx];
        case NC_INT32: return (double)((int32_t*)data)[idx];
        case NC_INT64: return (double)((int64_t*)data)[idx];
        case NC_UINT8: return (double)((uint8_t*)data)[idx];
        case NC_UINT16: return (double)((uint16_t*)data)[idx];
        case NC_UINT32: return (double)((uint32_t*)data)[idx];
        case NC_UINT64: return (double)((uint64_t*)data)[idx];
        case NC_FLOAT32: return (double)((float*)data)[idx];
        case NC_FLOAT64: return ((double*)data)[idx];
        default: return 0.0;
    }
}

static void nc_set_value_from_double(NCArray *arr, size_t linear_idx, double value) {
    char *data = (char *)arr->data;
    int64_t idx = 0, temp = linear_idx;
    for (int32_t d = arr->ndim - 1; d >= 0; d--) {
        idx += (temp % arr->shape[d]) * arr->strides[d];
        temp /= arr->shape[d];
    }
    switch (arr->dtype) {
        case NC_BOOL: ((bool*)data)[idx] = value != 0; break;
        case NC_INT8: ((int8_t*)data)[idx] = (int8_t)value; break;
        case NC_INT16: ((int16_t*)data)[idx] = (int16_t)value; break;
        case NC_INT32: ((int32_t*)data)[idx] = (int32_t)value; break;
        case NC_INT64: ((int64_t*)data)[idx] = (int64_t)value; break;
        case NC_UINT8: ((uint8_t*)data)[idx] = (uint8_t)value; break;
        case NC_UINT16: ((uint16_t*)data)[idx] = (uint16_t)value; break;
        case NC_UINT32: ((uint32_t*)data)[idx] = (uint32_t)value; break;
        case NC_UINT64: ((uint64_t*)data)[idx] = (uint64_t)value; break;
        case NC_FLOAT32: ((float*)data)[idx] = (float)value; break;
        case NC_FLOAT64: ((double*)data)[idx] = value; break;
        default: break;
    }
}

#define NC_BINARY_OP(name, op) \
NCArray *name(NCArray *a, NCArray *b) { \
    if (!a || !b) return NULL; \
    NCArray *result = nc_empty(a->ndim, a->shape, NC_FLOAT64); \
    if (!result) return NULL; \
    size_t total = nc_size(result); \
    for (size_t i = 0; i < total; i++) { \
        double av = nc_get_value_as_double(a, i); \
        double bv = nc_get_value_as_double(b, i); \
        ((double*)result->data)[i] = av op bv; \
    } \
    return result; \
}

NC_BINARY_OP(nc_add, +)
NC_BINARY_OP(nc_subtract, -)
NC_BINARY_OP(nc_multiply, *)
NC_BINARY_OP(nc_divide, /)

NCArray *nc_power(NCArray *a, NCArray *b) {
    if (!a || !b) return NULL;
    NCArray *result = nc_empty(a->ndim, a->shape, NC_FLOAT64);
    if (!result) return NULL;
    size_t total = nc_size(result);
    for (size_t i = 0; i < total; i++) {
        double av = nc_get_value_as_double(a, i);
        double bv = nc_get_value_as_double(b, i);
        ((double*)result->data)[i] = pow(av, bv);
    }
    return result;
}

NCArray *nc_mod(NCArray *a, NCArray *b) {
    if (!a || !b) return NULL;
    NCArray *result = nc_empty(a->ndim, a->shape, NC_FLOAT64);
    if (!result) return NULL;
    size_t total = nc_size(result);
    for (size_t i = 0; i < total; i++) {
        double av = nc_get_value_as_double(a, i);
        double bv = nc_get_value_as_double(b, i);
        ((double*)result->data)[i] = fmod(av, bv);
    }
    return result;
}

#define NC_COMPARE_OP(name, op) \
NCArray *name(NCArray *a, NCArray *b) { \
    if (!a || !b) return NULL; \
    NCArray *result = nc_empty(a->ndim, a->shape, NC_BOOL); \
    if (!result) return NULL; \
    size_t total = nc_size(result); \
    for (size_t i = 0; i < total; i++) { \
        double av = nc_get_value_as_double(a, i); \
        double bv = nc_get_value_as_double(b, i); \
        ((bool*)result->data)[i] = av op bv; \
    } \
    return result; \
}

NC_COMPARE_OP(nc_equal, ==)
NC_COMPARE_OP(nc_not_equal, !=)
NC_COMPARE_OP(nc_less, <)
NC_COMPARE_OP(nc_greater, >)
NC_COMPARE_OP(nc_less_equal, <=)
NC_COMPARE_OP(nc_greater_equal, >=)

NCArray *nc_logical_and(NCArray *a, NCArray *b) {
    if (!a || !b) return NULL;
    NCArray *result = nc_empty(a->ndim, a->shape, NC_BOOL);
    if (!result) return NULL;
    size_t total = nc_size(result);
    for (size_t i = 0; i < total; i++) {
        ((bool*)result->data)[i] = nc_get_value_as_double(a, i) != 0 && nc_get_value_as_double(b, i) != 0;
    }
    return result;
}

NCArray *nc_logical_or(NCArray *a, NCArray *b) {
    if (!a || !b) return NULL;
    NCArray *result = nc_empty(a->ndim, a->shape, NC_BOOL);
    if (!result) return NULL;
    size_t total = nc_size(result);
    for (size_t i = 0; i < total; i++) {
        ((bool*)result->data)[i] = nc_get_value_as_double(a, i) != 0 || nc_get_value_as_double(b, i) != 0;
    }
    return result;
}

NCArray *nc_logical_not(NCArray *a) {
    if (!a) return NULL;
    NCArray *result = nc_empty(a->ndim, a->shape, NC_BOOL);
    if (!result) return NULL;
    size_t total = nc_size(result);
    for (size_t i = 0; i < total; i++) {
        ((bool*)result->data)[i] = nc_get_value_as_double(a, i) == 0;
    }
    return result;
}

#define NC_UNARY_MATH_OP(name, func) \
NCArray *name(NCArray *arr) { \
    if (!arr) return NULL; \
    NCArray *result = nc_empty(arr->ndim, arr->shape, NC_FLOAT64); \
    if (!result) return NULL; \
    size_t total = nc_size(arr); \
    for (size_t i = 0; i < total; i++) { \
        ((double*)result->data)[i] = func(nc_get_value_as_double(arr, i)); \
    } \
    return result; \
}

NC_UNARY_MATH_OP(nc_abs, fabs)
NC_UNARY_MATH_OP(nc_floor, floor)
NC_UNARY_MATH_OP(nc_ceil, ceil)
NC_UNARY_MATH_OP(nc_round, round)
NC_UNARY_MATH_OP(nc_exp, exp)
NC_UNARY_MATH_OP(nc_log, log)
NC_UNARY_MATH_OP(nc_log10, log10)
NC_UNARY_MATH_OP(nc_sqrt, sqrt)
NC_UNARY_MATH_OP(nc_sin, sin)
NC_UNARY_MATH_OP(nc_cos, cos)
NC_UNARY_MATH_OP(nc_tan, tan)
NC_UNARY_MATH_OP(nc_arcsin, asin)
NC_UNARY_MATH_OP(nc_arccos, acos)
NC_UNARY_MATH_OP(nc_arctan, atan)

NCArray *nc_sign(NCArray *arr) {
    if (!arr) return NULL;
    NCArray *result = nc_empty(arr->ndim, arr->shape, arr->dtype);
    if (!result) return NULL;
    size_t total = nc_size(arr);
    for (size_t i = 0; i < total; i++) {
        double v = nc_get_value_as_double(arr, i);
        nc_set_value_from_double(result, i, (v > 0) - (v < 0));
    }
    return result;
}

NCArray *nc_negate(NCArray *arr) {
    if (!arr) return NULL;
    NCArray *result = nc_empty(arr->ndim, arr->shape, arr->dtype);
    if (!result) return NULL;
    size_t total = nc_size(arr);
    for (size_t i = 0; i < total; i++) {
        nc_set_value_from_double(result, i, -nc_get_value_as_double(arr, i));
    }
    return result;
}

NCArray *nc_dot(NCArray *a, NCArray *b) {
    if (!a || !b) return NULL;
    if (a->ndim == 1 && b->ndim == 1) {
        if (a->shape[0] != b->shape[0]) return NULL;
        NCArray *result = nc_zeros(0, NULL, NC_FLOAT64);
        if (!result) return NULL;
        double sum = 0;
        for (int64_t i = 0; i < a->shape[0]; i++) sum += nc_get_value_as_double(a, i) * nc_get_value_as_double(b, i);
        ((double*)result->data)[0] = sum;
        return result;
    }
    return nc_matmul(a, b);
}

NCArray *nc_matmul(NCArray *a, NCArray *b) {
    if (!a || !b) return NULL;
    if (a->ndim < 1 || b->ndim < 1) return NULL;
    int64_t a_rows = a->shape[a->ndim - 2];
    int64_t a_cols = a->shape[a->ndim - 1];
    int64_t b_rows = b->shape[b->ndim - 2];
    int64_t b_cols = b->shape[b->ndim - 1];
    if (a_cols != b_rows) return NULL;
    NCArray *result = nc_zeros(2, (int64_t[]){a_rows, b_cols}, NC_FLOAT64);
    if (!result) return NULL;
    for (int64_t i = 0; i < a_rows; i++) {
        for (int64_t j = 0; j < b_cols; j++) {
            double sum = 0;
            for (int64_t k = 0; k < a_cols; k++) {
                int64_t a_idx = i * a_cols + k;
                int64_t b_idx = k * b_cols + j;
                sum += nc_get_value_as_double(a, a_idx) * nc_get_value_as_double(b, b_idx);
            }
            ((double*)result->data)[i * b_cols + j] = sum;
        }
    }
    return result;
}

NCArray *nc_inner(NCArray *a, NCArray *b) {
    if (!a || !b) return NULL;
    NCArray *result = nc_zeros(0, NULL, NC_FLOAT64);
    if (!result) return NULL;
    double sum = 0;
    size_t total = nc_size(a);
    for (size_t i = 0; i < total; i++) sum += nc_get_value_as_double(a, i) * nc_get_value_as_double(b, i);
    ((double*)result->data)[0] = sum;
    return result;
}

NCArray *nc_outer(NCArray *a, NCArray *b) {
    if (!a || !b || a->ndim != 1 || b->ndim != 1) return NULL;
    NCArray *result = nc_empty(2, (int64_t[]){a->shape[0], b->shape[0]}, NC_FLOAT64);
    if (!result) return NULL;
    double *rdata = (double *)result->data;
    for (int64_t i = 0; i < a->shape[0]; i++) {
        double av = nc_get_value_as_double(a, i);
        for (int64_t j = 0; j < b->shape[0]; j++) {
            rdata[i * b->shape[0] + j] = av * nc_get_value_as_double(b, j);
        }
    }
    return result;
}

NCArray *nc_cross(NCArray *a, NCArray *b, int32_t axis) {
    if (!a || !b || a->ndim != 1 || b->ndim != 1) return NULL;
    if (a->shape[0] != 3 || b->shape[0] != 3) return NULL;
    NCArray *result = nc_empty(1, (int64_t[]){3}, NC_FLOAT64);
    if (!result) return NULL;
    double *r = (double *)result->data;
    double a0 = nc_get_value_as_double(a, 0), a1 = nc_get_value_as_double(a, 1), a2 = nc_get_value_as_double(a, 2);
    double b0 = nc_get_value_as_double(b, 0), b1 = nc_get_value_as_double(b, 1), b2 = nc_get_value_as_double(b, 2);
    r[0] = a1 * b2 - a2 * b1;
    r[1] = a2 * b0 - a0 * b2;
    r[2] = a0 * b1 - a1 * b0;
    return result;
}

NCArray *nc_trace(NCArray *arr, int32_t offset, int32_t axis1, int32_t axis2) {
    if (!arr || arr->ndim < 2) return NULL;
    int64_t n = arr->shape[axis1];
    int64_t m = arr->shape[axis2];
    int64_t k = (offset >= 0) ? offset : -offset;
    int64_t diag_len = (n < m - k) ? n : m - k;
    if (diag_len < 0) diag_len = 0;
    NCArray *result = nc_zeros(1, (int64_t[]){diag_len}, arr->dtype);
    if (!result) return NULL;
    char *src = (char *)arr->data, *dst = (char *)result->data;
    size_t esize = arr->itemsize;
    int64_t stride1 = arr->strides[axis1], stride2 = arr->strides[axis2];
    for (int64_t i = 0; i < diag_len; i++) {
        int64_t row = (offset >= 0) ? i : i - offset;
        int64_t col = (offset >= 0) ? i + offset : i;
        memcpy(dst + i * esize, src + (row * stride1 + col * stride2) * esize, esize);
    }
    return result;
}

NCArray *nc_sum(NCArray *arr, const int32_t *axis, int32_t naxis) {
    if (!arr) return NULL;
    NCArray *result = nc_zeros(0, NULL, NC_FLOAT64);
    if (!result) return NULL;
    double sum = 0;
    size_t total = nc_size(arr);
    for (size_t i = 0; i < total; i++) sum += nc_get_value_as_double(arr, i);
    ((double*)result->data)[0] = sum;
    return result;
}

NCArray *nc_prod(NCArray *arr, const int32_t *axis, int32_t naxis) {
    if (!arr) return NULL;
    NCArray *result = nc_zeros(0, NULL, NC_FLOAT64);
    if (!result) return NULL;
    double prod = 1;
    size_t total = nc_size(arr);
    for (size_t i = 0; i < total; i++) prod *= nc_get_value_as_double(arr, i);
    ((double*)result->data)[0] = prod;
    return result;
}

NCArray *nc_mean(NCArray *arr, const int32_t *axis, int32_t naxis) {
    if (!arr) return NULL;
    NCArray *sum = nc_sum(arr, axis, naxis);
    if (!sum) return NULL;
    ((double*)sum->data)[0] /= nc_size(arr);
    return sum;
}

NCArray *nc_var(NCArray *arr, const int32_t *axis, int32_t naxis) {
    if (!arr) return NULL;
    NCArray *mean = nc_mean(arr, axis, naxis);
    if (!mean) return NULL;
    NCArray *result = nc_zeros(0, NULL, NC_FLOAT64);
    if (!result) return NULL;
    double mu = ((double*)mean->data)[0], var = 0;
    size_t total = nc_size(arr);
    for (size_t i = 0; i < total; i++) {
        double diff = nc_get_value_as_double(arr, i) - mu;
        var += diff * diff;
    }
    ((double*)result->data)[0] = var / total;
    nc_release(mean);
    return result;
}

NCArray *nc_std(NCArray *arr, const int32_t *axis, int32_t naxis) {
    if (!arr) return NULL;
    NCArray *v = nc_var(arr, axis, naxis);
    if (!v) return NULL;
    ((double*)v->data)[0] = sqrt(((double*)v->data)[0]);
    return v;
}

NCArray *nc_min(NCArray *arr, const int32_t *axis, int32_t naxis) {
    if (!arr) return NULL;
    NCArray *result = nc_zeros(0, NULL, NC_FLOAT64);
    if (!result) return NULL;
    double min_val = INFINITY;
    size_t total = nc_size(arr);
    for (size_t i = 0; i < total; i++) {
        double v = nc_get_value_as_double(arr, i);
        if (v < min_val) min_val = v;
    }
    ((double*)result->data)[0] = min_val;
    return result;
}

NCArray *nc_max(NCArray *arr, const int32_t *axis, int32_t naxis) {
    if (!arr) return NULL;
    NCArray *result = nc_zeros(0, NULL, NC_FLOAT64);
    if (!result) return NULL;
    double max_val = -INFINITY;
    size_t total = nc_size(arr);
    for (size_t i = 0; i < total; i++) {
        double v = nc_get_value_as_double(arr, i);
        if (v > max_val) max_val = v;
    }
    ((double*)result->data)[0] = max_val;
    return result;
}

NCArray *nc_argmin(NCArray *arr, int32_t axis) {
    if (!arr) return NULL;
    NCArray *result = nc_zeros(1, (int64_t[]){nc_size(arr)}, NC_INT64);
    if (!result) return NULL;
    int64_t *rdata = (int64_t*)result->data;
    size_t total = nc_size(arr);
    int64_t min_idx = 0;
    double min_val = INFINITY;
    for (size_t i = 0; i < total; i++) {
        double v = nc_get_value_as_double(arr, i);
        if (v < min_val) { min_val = v; min_idx = i; }
    }
    rdata[0] = min_idx;
    return result;
}

NCArray *nc_argmax(NCArray *arr, int32_t axis) {
    if (!arr) return NULL;
    NCArray *result = nc_zeros(1, (int64_t[]){nc_size(arr)}, NC_INT64);
    if (!result) return NULL;
    int64_t *rdata = (int64_t*)result->data;
    size_t total = nc_size(arr);
    int64_t max_idx = 0;
    double max_val = -INFINITY;
    for (size_t i = 0; i < total; i++) {
        double v = nc_get_value_as_double(arr, i);
        if (v > max_val) { max_val = v; max_idx = i; }
    }
    rdata[0] = max_idx;
    return result;
}

NCArray *nc_all(NCArray *arr, const int32_t *axis, int32_t naxis) {
    if (!arr) return NULL;
    NCArray *result = nc_zeros(0, NULL, NC_BOOL);
    if (!result) return NULL;
    size_t total = nc_size(arr);
    bool all_true = true;
    for (size_t i = 0; i < total; i++) if (!nc_get_value_as_double(arr, i)) { all_true = false; break; }
    ((bool*)result->data)[0] = all_true;
    return result;
}

NCArray *nc_any(NCArray *arr, const int32_t *axis, int32_t naxis) {
    if (!arr) return NULL;
    NCArray *result = nc_zeros(0, NULL, NC_BOOL);
    if (!result) return NULL;
    size_t total = nc_size(arr);
    bool any_true = false;
    for (size_t i = 0; i < total; i++) if (nc_get_value_as_double(arr, i)) { any_true = true; break; }
    ((bool*)result->data)[0] = any_true;
    return result;
}

NCArray *nc_cumsum(NCArray *arr, int32_t axis) { return nc_copy(arr); }

int64_t nc_count_nonzero(NCArray *arr) {
    if (!arr) return 0;
    size_t total = nc_size(arr);
    int64_t count = 0;
    for (size_t i = 0; i < total; i++) if (nc_get_value_as_double(arr, i) != 0) count++;
    return count;
}

bool nc_isnan(NCArray *arr) {
    if (!arr) return false;
    size_t total = nc_size(arr);
    for (size_t i = 0; i < total; i++) if (isnan(nc_get_value_as_double(arr, i))) return true;
    return false;
}

bool nc_isfinite(NCArray *arr) {
    if (!arr) return false;
    size_t total = nc_size(arr);
    for (size_t i = 0; i < total; i++) if (!isfinite(nc_get_value_as_double(arr, i))) return false;
    return true;
}

NCArray *nc_concatenate(NCArray **arrays, int32_t n, int32_t axis) {
    if (!arrays || n <= 0) return NULL;
    if (axis < 0) axis = arrays[0]->ndim - 1;
    for (int32_t i = 1; i < n; i++) {
        if (arrays[i]->ndim != arrays[0]->ndim) return NULL;
        for (int32_t j = 0; j < arrays[0]->ndim; j++)
            if (j != axis && arrays[i]->shape[j] != arrays[0]->shape[j]) return NULL;
    }
    int64_t total_size = 0;
    for (int32_t i = 0; i < n; i++) total_size += arrays[i]->shape[axis];
    int32_t ndim = arrays[0]->ndim;
    int64_t result_shape[NC_MAX_DIMS];
    for (int32_t i = 0; i < ndim; i++) result_shape[i] = (i == axis) ? total_size : arrays[0]->shape[i];
    NCArray *result = nc_empty(ndim, result_shape, arrays[0]->dtype);
    if (!result) return NULL;
    char *dst = (char *)result->data;
    size_t esize = result->itemsize;
    int64_t offset = 0;
    for (int32_t i = 0; i < n; i++) {
        size_t arr_size = nc_size(arrays[i]);
        memcpy(dst + offset * esize, arrays[i]->data, arr_size * esize);
        offset += arrays[i]->shape[axis];
    }
    return result;
}

NCArray *nc_stack(NCArray **arrays, int32_t n, int32_t axis) {
    if (!arrays || n <= 0) return NULL;
    if (axis < 0) axis = arrays[0]->ndim;
    int32_t result_ndim = arrays[0]->ndim + 1;
    int64_t result_shape[NC_MAX_DIMS];
    for (int32_t i = 0; i < axis; i++) result_shape[i] = arrays[0]->shape[i];
    result_shape[axis] = n;
    for (int32_t i = axis + 1; i < result_ndim; i++) result_shape[i] = arrays[0]->shape[i - 1];
    NCArray *result = nc_empty(result_ndim, result_shape, arrays[0]->dtype);
    if (!result) return NULL;
    size_t esize = result->itemsize;
    size_t single_size = nc_size(arrays[0]);
    for (int32_t i = 0; i < n; i++) {
        int64_t offset = 0, temp = i;
        for (int32_t d = result_ndim - 1; d >= 0; d--) {
            if (d == axis) { offset += temp % result_shape[d]; temp /= result_shape[d]; }
            else {
                int32_t arr_dim = (d > axis) ? d - 1 : d;
                offset += (temp % arrays[0]->shape[arr_dim]) * arrays[0]->strides[arr_dim];
                temp /= arrays[0]->shape[arr_dim];
            }
        }
        memcpy((char*)result->data + offset * esize, arrays[i]->data, single_size * esize);
    }
    return result;
}

static uint64_t nc_random_state = 1;

NCArray *nc_random_rand(int32_t ndim, const int64_t *shape) {
    NCArray *arr = nc_empty(ndim, shape, NC_FLOAT64);
    if (!arr) return NULL;
    double *data = (double*)arr->data;
    size_t total = nc_size(arr);
    for (size_t i = 0; i < total; i++) data[i] = (double)rand() / RAND_MAX;
    return arr;
}

NCArray *nc_random_randn(int32_t ndim, const int64_t *shape, NCDataType dtype) {
    NCArray *arr = nc_empty(ndim, shape, dtype);
    if (!arr) return NULL;
    size_t total = nc_size(arr);
    for (size_t i = 0; i < total; i++) {
        double u1 = (double)rand() / RAND_MAX;
        double u2 = (double)rand() / RAND_MAX;
        double g = sqrt(-2.0 * log(u1)) * cos(2.0 * M_PI * u2);
        if (dtype == NC_FLOAT32) ((float*)arr->data)[i] = (float)g;
        else ((double*)arr->data)[i] = g;
    }
    return arr;
}

NCArray *nc_random_randint(int64_t low, int64_t high, int32_t ndim, const int64_t *shape) {
    NCArray *arr = nc_empty(ndim, shape, NC_INT64);
    if (!arr) return NULL;
    int64_t *data = (int64_t*)arr->data;
    size_t total = nc_size(arr);
    for (size_t i = 0; i < total; i++) data[i] = low + (int64_t)((high - low) * (double)rand() / RAND_MAX);
    return arr;
}

void nc_random_seed(uint64_t seed) { nc_random_state = seed; srand((unsigned int)seed); }

void nc_random_shuffle(NCArray *arr) {
    if (!arr) return;
    size_t total = nc_size(arr);
    for (size_t i = total - 1; i > 0; i--) {
        size_t j = (size_t)((i + 1) * (double)rand() / RAND_MAX);
        double temp = nc_get_value_as_double(arr, i);
        nc_set_value_from_double(arr, i, nc_get_value_as_double(arr, j));
        nc_set_value_from_double(arr, j, temp);
    }
}

NCArray *nc_linalg_norm(NCArray *arr, const char *ord) {
    if (!arr) return NULL;
    NCArray *result = nc_zeros(0, NULL, NC_FLOAT64);
    if (!result) return NULL;
    double sum = 0;
    size_t total = nc_size(arr);
    for (size_t i = 0; i < total; i++) { double v = nc_get_value_as_double(arr, i); sum += v * v; }
    ((double*)result->data)[0] = sqrt(sum);
    return result;
}

static NCDataType nc_fixed_best_dtype(int int_bits, int frac_bits, bool is_signed) {
    int total_bits = int_bits + frac_bits;
    if (is_signed) {
        if (total_bits <= 8) return NC_INT8;
        if (total_bits <= 16) return NC_INT16;
        if (total_bits <= 32) return NC_INT32;
        return NC_INT64;
    } else {
        if (total_bits <= 8) return NC_UINT8;
        if (total_bits <= 16) return NC_UINT16;
        if (total_bits <= 32) return NC_UINT32;
        return NC_UINT64;
    }
}

int64_t nc_fixed_from_double(double value, int frac_bits) {
    double scaled = value * (double)(1LL << frac_bits);
    if (scaled > 0) scaled += 0.5;
    else scaled -= 0.5;
    return (int64_t)scaled;
}

double nc_fixed_to_double(int64_t raw, int frac_bits) {
    return (double)raw / (double)(1LL << frac_bits);
}

double nc_fixed_range_min(int int_bits, int frac_bits, bool is_signed) {
    if (is_signed) {
        int64_t min_val = -(1LL << (int_bits + frac_bits - 1));
        return (double)min_val / (double)(1LL << frac_bits);
    }
    return 0.0;
}

double nc_fixed_range_max(int int_bits, int frac_bits, bool is_signed) {
    if (is_signed) {
        int64_t max_val = (1LL << (int_bits + frac_bits - 1)) - 1;
        return (double)max_val / (double)(1LL << frac_bits);
    } else {
        uint64_t max_val = (1ULL << (int_bits + frac_bits)) - 1;
        return (double)max_val / (double)(1LL << frac_bits);
    }
}

NCArray *nc_fixed_create(int int_bits, int frac_bits, bool is_signed, int32_t ndim, const int64_t *shape) {
    NCDataType dtype = nc_fixed_best_dtype(int_bits, frac_bits, is_signed);
    NCArray *arr = nc_empty(ndim, shape, dtype);
    return arr;
}

NCArray *nc_fixed_zeros(int int_bits, int frac_bits, bool is_signed, int32_t ndim, const int64_t *shape) {
    NCDataType dtype = nc_fixed_best_dtype(int_bits, frac_bits, is_signed);
    NCArray *arr = nc_zeros(ndim, shape, dtype);
    return arr;
}

NCArray *nc_fixed_from_values(int int_bits, int frac_bits, bool is_signed, double *values, size_t count) {
    NCDataType dtype = nc_fixed_best_dtype(int_bits, frac_bits, is_signed);
    int64_t shape[1] = {(int64_t)count};
    NCArray *arr = nc_empty(1, shape, dtype);
    if (!arr) return NULL;
    for (size_t i = 0; i < count; i++) {
        int64_t raw = nc_fixed_from_double(values[i], frac_bits);
        switch (dtype) {
            case NC_INT8: ((int8_t*)arr->data)[i] = (int8_t)raw; break;
            case NC_INT16: ((int16_t*)arr->data)[i] = (int16_t)raw; break;
            case NC_INT32: ((int32_t*)arr->data)[i] = (int32_t)raw; break;
            case NC_INT64: ((int64_t*)arr->data)[i] = raw; break;
            case NC_UINT8: ((uint8_t*)arr->data)[i] = (uint8_t)raw; break;
            case NC_UINT16: ((uint16_t*)arr->data)[i] = (uint16_t)raw; break;
            case NC_UINT32: ((uint32_t*)arr->data)[i] = (uint32_t)raw; break;
            case NC_UINT64: ((uint64_t*)arr->data)[i] = (uint64_t)raw; break;
            default: break;
        }
    }
    return arr;
}

NCArray *nc_fixed_arange(double start, double stop, double step, int int_bits, int frac_bits, bool is_signed) {
    if (step == 0) return NULL;
    int64_t n = (int64_t)ceil((stop - start) / step);
    if (n < 0) n = 0;
    int64_t shape[1] = {n};
    NCDataType dtype = nc_fixed_best_dtype(int_bits, frac_bits, is_signed);
    NCArray *arr = nc_empty(1, shape, dtype);
    if (!arr) return NULL;
    for (int64_t i = 0; i < n; i++) {
        double val = start + i * step;
        int64_t raw = nc_fixed_from_double(val, frac_bits);
        switch (dtype) {
            case NC_INT8: ((int8_t*)arr->data)[i] = (int8_t)raw; break;
            case NC_INT16: ((int16_t*)arr->data)[i] = (int16_t)raw; break;
            case NC_INT32: ((int32_t*)arr->data)[i] = (int32_t)raw; break;
            case NC_INT64: ((int64_t*)arr->data)[i] = raw; break;
            case NC_UINT8: ((uint8_t*)arr->data)[i] = (uint8_t)raw; break;
            case NC_UINT16: ((uint16_t*)arr->data)[i] = (uint16_t)raw; break;
            case NC_UINT32: ((uint32_t*)arr->data)[i] = (uint32_t)raw; break;
            case NC_UINT64: ((uint64_t*)arr->data)[i] = (uint64_t)raw; break;
            default: break;
        }
    }
    return arr;
}

NCArray *nc_fixed_random_rand(int int_bits, int frac_bits, bool is_signed, int32_t ndim, const int64_t *shape) {
    NCDataType dtype = nc_fixed_best_dtype(int_bits, frac_bits, is_signed);
    NCArray *arr = nc_empty(ndim, shape, dtype);
    if (!arr) return NULL;
    size_t total = nc_size(arr);
    int total_bits = int_bits + frac_bits;
    if (is_signed) {
        int64_t min_val = -(1LL << (total_bits - 1));
        int64_t max_val = (1LL << (total_bits - 1)) - 1;
        int64_t range = max_val - min_val + 1;
        for (size_t i = 0; i < total; i++) {
            int64_t raw = min_val + (int64_t)((double)range * rand() / (RAND_MAX + 1.0));
            switch (dtype) {
                case NC_INT8: ((int8_t*)arr->data)[i] = (int8_t)raw; break;
                case NC_INT16: ((int16_t*)arr->data)[i] = (int16_t)raw; break;
                case NC_INT32: ((int32_t*)arr->data)[i] = (int32_t)raw; break;
                case NC_INT64: ((int64_t*)arr->data)[i] = raw; break;
                default: break;
            }
        }
    } else {
        uint64_t max_val = (1ULL << total_bits) - 1;
        uint64_t range = max_val + 1;
        for (size_t i = 0; i < total; i++) {
            uint64_t raw = (uint64_t)((double)range * rand() / (RAND_MAX + 1.0));
            switch (dtype) {
                case NC_UINT8: ((uint8_t*)arr->data)[i] = (uint8_t)raw; break;
                case NC_UINT16: ((uint16_t*)arr->data)[i] = (uint16_t)raw; break;
                case NC_UINT32: ((uint32_t*)arr->data)[i] = (uint32_t)raw; break;
                case NC_UINT64: ((uint64_t*)arr->data)[i] = raw; break;
                default: break;
            }
        }
    }
    return arr;
}

NCArray *nc_fixed_random_uniform(int int_bits, int frac_bits, bool is_signed, double min_val, double max_val, int32_t ndim, const int64_t *shape) {
    NCDataType dtype = nc_fixed_best_dtype(int_bits, frac_bits, is_signed);
    NCArray *arr = nc_empty(ndim, shape, dtype);
    if (!arr) return NULL;
    size_t total = nc_size(arr);
    for (size_t i = 0; i < total; i++) {
        double u = (double)rand() / RAND_MAX;
        double val = min_val + u * (max_val - min_val);
        int64_t raw = nc_fixed_from_double(val, frac_bits);
        switch (dtype) {
            case NC_INT8: ((int8_t*)arr->data)[i] = (int8_t)raw; break;
            case NC_INT16: ((int16_t*)arr->data)[i] = (int16_t)raw; break;
            case NC_INT32: ((int32_t*)arr->data)[i] = (int32_t)raw; break;
            case NC_INT64: ((int64_t*)arr->data)[i] = raw; break;
            case NC_UINT8: ((uint8_t*)arr->data)[i] = (uint8_t)raw; break;
            case NC_UINT16: ((uint16_t*)arr->data)[i] = (uint16_t)raw; break;
            case NC_UINT32: ((uint32_t*)arr->data)[i] = (uint32_t)raw; break;
            case NC_UINT64: ((uint64_t*)arr->data)[i] = (uint64_t)raw; break;
            default: break;
        }
    }
    return arr;
}

double nc_fixed_get_value_as_double(NCArray *arr, size_t idx, int frac_bits) {
    if (!arr) return 0.0;
    int64_t raw = 0;
    switch (arr->dtype) {
        case NC_INT8: raw = ((int8_t*)arr->data)[idx]; break;
        case NC_INT16: raw = ((int16_t*)arr->data)[idx]; break;
        case NC_INT32: raw = ((int32_t*)arr->data)[idx]; break;
        case NC_INT64: raw = ((int64_t*)arr->data)[idx]; break;
        case NC_UINT8: raw = ((uint8_t*)arr->data)[idx]; break;
        case NC_UINT16: raw = ((uint16_t*)arr->data)[idx]; break;
        case NC_UINT32: raw = ((uint32_t*)arr->data)[idx]; break;
        case NC_UINT64: raw = ((uint64_t*)arr->data)[idx]; break;
        default: return 0.0;
    }
    return nc_fixed_to_double(raw, frac_bits);
}

void nc_fixed_print(NCArray *arr, int frac_bits) {
    if (!arr) { printf("NULL array\n"); return; }
    printf("fixed-point([");
    size_t total = nc_size(arr);
    for (size_t i = 0; i < total; i++) {
        if (i > 0) printf(" ");
        printf("%.6g", nc_fixed_get_value_as_double(arr, i, frac_bits));
        if (i < total - 1) printf(",");
    }
    printf("], shape=%d, frac_bits=%d, dtype=%s)\n", arr->ndim, frac_bits, nc_dtype_name(arr->dtype));
}

NCArray *nc_fixed_add(NCArray *a, NCArray *b, int frac_bits) {
    if (!a || !b) return NULL;
    NCArray *result = nc_empty(a->ndim, a->shape, a->dtype);
    if (!result) return NULL;
    size_t total = nc_size(a);
    for (size_t i = 0; i < total; i++) {
        double av = nc_fixed_get_value_as_double(a, i, frac_bits);
        double bv = nc_fixed_get_value_as_double(b, i, frac_bits);
        int64_t raw = nc_fixed_from_double(av + bv, frac_bits);
        switch (result->dtype) {
            case NC_INT8: ((int8_t*)result->data)[i] = (int8_t)raw; break;
            case NC_INT16: ((int16_t*)result->data)[i] = (int16_t)raw; break;
            case NC_INT32: ((int32_t*)result->data)[i] = (int32_t)raw; break;
            case NC_INT64: ((int64_t*)result->data)[i] = raw; break;
            case NC_UINT8: ((uint8_t*)result->data)[i] = (uint8_t)raw; break;
            case NC_UINT16: ((uint16_t*)result->data)[i] = (uint16_t)raw; break;
            case NC_UINT32: ((uint32_t*)result->data)[i] = (uint32_t)raw; break;
            case NC_UINT64: ((uint64_t*)result->data)[i] = (uint64_t)raw; break;
            default: break;
        }
    }
    return result;
}

NCArray *nc_fixed_multiply(NCArray *a, NCArray *b, int a_frac_bits, int b_frac_bits, int result_frac_bits, NCDataType result_dtype) {
    if (!a || !b) return NULL;
    NCArray *result = nc_empty(a->ndim, a->shape, result_dtype);
    if (!result) return NULL;
    size_t total = nc_size(a);
    for (size_t i = 0; i < total; i++) {
        double av = nc_fixed_get_value_as_double(a, i, a_frac_bits);
        double bv = nc_fixed_get_value_as_double(b, i, b_frac_bits);
        int64_t raw = nc_fixed_from_double(av * bv, result_frac_bits);
        switch (result->dtype) {
            case NC_INT8: ((int8_t*)result->data)[i] = (int8_t)raw; break;
            case NC_INT16: ((int16_t*)result->data)[i] = (int16_t)raw; break;
            case NC_INT32: ((int32_t*)result->data)[i] = (int32_t)raw; break;
            case NC_INT64: ((int64_t*)result->data)[i] = raw; break;
            case NC_UINT8: ((uint8_t*)result->data)[i] = (uint8_t)raw; break;
            case NC_UINT16: ((uint16_t*)result->data)[i] = (uint16_t)raw; break;
            case NC_UINT32: ((uint32_t*)result->data)[i] = (uint32_t)raw; break;
            case NC_UINT64: ((uint64_t*)result->data)[i] = (uint64_t)raw; break;
            default: break;
        }
    }
    return result;
}

void nc_print(NCArray *arr) {
    if (!arr) { printf("NULL array\n"); return; }
    printf("array([");
    size_t total = nc_size(arr);
    for (size_t i = 0; i < total; i++) {
        if (i > 0) printf(" ");
        printf("%.6g", nc_get_value_as_double(arr, i));
        if (i < total - 1) printf(",");
    }
    printf("], shape=%d, dtype=%s)\n", arr->ndim, nc_dtype_name(arr->dtype));
}

NCArray *nc_retain(NCArray *arr) { if (!arr) return NULL; arr->refcount++; return arr; }

void nc_release(NCArray *arr) {
    if (!arr) return;
    arr->refcount--;
    if (arr->refcount <= 0) {
        if (arr->owns_data && arr->data) free(arr->data);
        free(arr);
    }
}

NCStatus nc_save(const char *filename, NCArray *arr) {
    if (!filename || !arr) return NC_ERROR;
    FILE *fp = fopen(filename, "wb");
    if (!fp) return NC_ERROR;
    fwrite(&arr->ndim, sizeof(int32_t), 1, fp);
    fwrite(arr->shape, sizeof(int64_t), arr->ndim, fp);
    fwrite(&arr->dtype, sizeof(NCDataType), 1, fp);
    fwrite(arr->data, arr->itemsize, nc_size(arr), fp);
    fclose(fp);
    return NC_OK;
}

NCArray *nc_load(const char *filename) {
    if (!filename) return NULL;
    FILE *fp = fopen(filename, "rb");
    if (!fp) return NULL;
    int32_t ndim;
    if (fread(&ndim, sizeof(int32_t), 1, fp) != 1) { fclose(fp); return NULL; }
    int64_t shape[NC_MAX_DIMS];
    if (fread(shape, sizeof(int64_t), ndim, fp) != (size_t)ndim) { fclose(fp); return NULL; }
    NCDataType dtype;
    if (fread(&dtype, sizeof(NCDataType), 1, fp) != 1) { fclose(fp); return NULL; }
    NCArray *arr = nc_empty(ndim, shape, dtype);
    if (!arr) { fclose(fp); return NULL; }
    size_t total = nc_size(arr);
    if (fread(arr->data, arr->itemsize, total, fp) != total) { nc_release(arr); fclose(fp); return NULL; }
    fclose(fp);
    return arr;
}

static double nc_va_arg_double(va_list *ap, NCDataType dtype) {
    switch (dtype) {
        case NC_BOOL: return (double)va_arg(*ap, int);
        case NC_INT8: case NC_INT16: case NC_INT32: return (double)va_arg(*ap, int);
        case NC_INT64: return (double)va_arg(*ap, long long);
        case NC_UINT8: case NC_UINT16: case NC_UINT32: return (double)va_arg(*ap, unsigned int);
        case NC_UINT64: return (double)va_arg(*ap, unsigned long long);
        case NC_FLOAT32: case NC_FLOAT64: return va_arg(*ap, double);
        default: return 0.0;
    }
}

NCArray *nc_make_1d(NCDataType dtype, int64_t n, ...) {
    if (n <= 0) return nc_empty(1, (int64_t[]){0}, dtype);
    int64_t shape[1] = {n};
    NCArray *arr = nc_empty(1, shape, dtype);
    if (!arr) return NULL;
    va_list args; va_start(args, n);
    for (int64_t i = 0; i < n; i++) nc_set_value_from_double(arr, i, nc_va_arg_double(&args, dtype));
    va_end(args);
    return arr;
}

NCArray *nc_make_2d(NCDataType dtype, int64_t rows, int64_t cols, ...) {
    if (rows <= 0 || cols <= 0) return nc_empty(2, (int64_t[]){rows, cols}, dtype);
    int64_t shape[2] = {rows, cols};
    NCArray *arr = nc_empty(2, shape, dtype);
    if (!arr) return NULL;
    va_list args; va_start(args, cols);
    for (int64_t i = 0; i < rows; i++) for (int64_t j = 0; j < cols; j++) nc_set_value_from_double(arr, i * cols + j, nc_va_arg_double(&args, dtype));
    va_end(args);
    return arr;
}

NCArray *nc_make_1d_auto(int n, ...) {
    if (n <= 0) return nc_empty(1, (int64_t[]){0}, NC_INT64);
    NCDataType dtype = NC_INT64;
    bool all_positive = true, fits_int32 = true, fits_int16 = true, fits_int8 = true;
    va_list args, args_copy;
    va_start(args, n); va_copy(args_copy, args);
    for (int i = 0; i < n; i++) {
        int64_t v = va_arg(args, int64_t);
        if (v < 0) all_positive = false;
        if (v > INT32_MAX || v < INT32_MIN) fits_int32 = false;
        if (v > INT16_MAX || v < INT16_MIN) fits_int16 = false;
        if (v > INT8_MAX || v < INT8_MIN) fits_int8 = false;
    }
    va_end(args);
    if (all_positive) {
        bool fits_uint32 = true, fits_uint16 = true, fits_uint8 = true;
        va_start(args_copy, n);
        for (int i = 0; i < n; i++) {
            int64_t v = va_arg(args_copy, int64_t);
            if (v > UINT32_MAX) fits_uint32 = false;
            if (v > UINT16_MAX) fits_uint16 = false;
            if (v > UINT8_MAX) fits_uint8 = false;
        }
        va_end(args_copy);
        if (fits_uint8) dtype = NC_UINT8;
        else if (fits_uint16) dtype = NC_UINT16;
        else if (fits_uint32) dtype = NC_UINT32;
        else dtype = NC_INT64;
    } else {
        if (fits_int8) dtype = NC_INT8;
        else if (fits_int16) dtype = NC_INT16;
        else if (fits_int32) dtype = NC_INT32;
        else dtype = NC_INT64;
    }
    NCArray *arr = nc_empty(1, (int64_t[]){n}, dtype);
    if (!arr) return NULL;
    va_start(args_copy, n);
    for (int i = 0; i < n; i++) nc_set_value_from_double(arr, i, (double)va_arg(args_copy, int64_t));
    va_end(args_copy);
    return arr;
}

NCArray *nc_make_2d_auto(int64_t rows, int64_t cols, int n, ...) {
    if (rows <= 0 || cols <= 0) return nc_empty(2, (int64_t[]){rows, cols}, NC_INT64);
    NCDataType dtype = NC_INT64;
    bool all_positive = true, fits_int32 = true, fits_int16 = true, fits_int8 = true;
    va_list args, args_copy;
    va_start(args, n); va_copy(args_copy, args);
    for (int i = 0; i < n; i++) {
        int64_t v = va_arg(args, int64_t);
        if (v < 0) all_positive = false;
        if (v > INT32_MAX || v < INT32_MIN) fits_int32 = false;
        if (v > INT16_MAX || v < INT16_MIN) fits_int16 = false;
        if (v > INT8_MAX || v < INT8_MIN) fits_int8 = false;
    }
    va_end(args);
    if (all_positive) {
        bool fits_uint32 = true, fits_uint16 = true, fits_uint8 = true;
        va_start(args_copy, n);
        for (int i = 0; i < n; i++) {
            int64_t v = va_arg(args_copy, int64_t);
            if (v > UINT32_MAX) fits_uint32 = false;
            if (v > UINT16_MAX) fits_uint16 = false;
            if (v > UINT8_MAX) fits_uint8 = false;
        }
        va_end(args_copy);
        if (fits_uint8) dtype = NC_UINT8;
        else if (fits_uint16) dtype = NC_UINT16;
        else if (fits_uint32) dtype = NC_UINT32;
        else dtype = NC_INT64;
    } else {
        if (fits_int8) dtype = NC_INT8;
        else if (fits_int16) dtype = NC_INT16;
        else if (fits_int32) dtype = NC_INT32;
        else dtype = NC_INT64;
    }
    NCArray *arr = nc_empty(2, (int64_t[]){rows, cols}, dtype);
    if (!arr) return NULL;
    va_start(args_copy, n);
    for (int i = 0; i < n; i++) nc_set_value_from_double(arr, i, (double)va_arg(args_copy, int64_t));
    va_end(args_copy);
    return arr;
}

NCArray *nc_make_1d_float_auto(int n, ...) {
    if (n <= 0) return nc_empty(1, (int64_t[]){0}, NC_FLOAT32);
    NCDataType dtype = NC_FLOAT32;
    va_list args, args_copy;
    va_start(args, n); va_copy(args_copy, args);
    for (int i = 0; i < n; i++) {
        double v = va_arg(args, double);
        float fv = (float)v;
        if (fabs(v - (double)fv) > 1e-6 * fabs(v > 0 ? v : -v)) { dtype = NC_FLOAT64; break; }
        if (fabs(v) > FLT_MAX || (fabs(v) < FLT_MIN && v != 0)) { dtype = NC_FLOAT64; break; }
    }
    va_end(args);
    NCArray *arr = nc_empty(1, (int64_t[]){n}, dtype);
    if (!arr) return NULL;
    va_start(args_copy, n);
    for (int i = 0; i < n; i++) nc_set_value_from_double(arr, i, va_arg(args_copy, double));
    va_end(args_copy);
    return arr;
}

NCArray *nc_make_2d_float_auto(int64_t rows, int64_t cols, int n, ...) {
    if (rows <= 0 || cols <= 0) return nc_empty(2, (int64_t[]){rows, cols}, NC_FLOAT32);
    NCDataType dtype = NC_FLOAT32;
    va_list args, args_copy;
    va_start(args, n); va_copy(args_copy, args);
    for (int i = 0; i < n; i++) {
        double v = va_arg(args, double);
        float fv = (float)v;
        if (fabs(v - (double)fv) > 1e-6 * fabs(v > 0 ? v : -v)) { dtype = NC_FLOAT64; break; }
        if (fabs(v) > FLT_MAX || (fabs(v) < FLT_MIN && v != 0)) { dtype = NC_FLOAT64; break; }
    }
    va_end(args);
    NCArray *arr = nc_empty(2, (int64_t[]){rows, cols}, dtype);
    if (!arr) return NULL;
    va_start(args_copy, n);
    for (int i = 0; i < n; i++) nc_set_value_from_double(arr, i, va_arg(args_copy, double));
    va_end(args_copy);
    return arr;
}

#endif
