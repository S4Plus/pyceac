# Checkers and warnings for bug patterns

The order is a litte different from the paper.

| number | pattern | Done |
| ------ | ------- | ---- |
| 1      | mishandling exceptions | Y |
| 2      | insufficient error checking | Y |
| 3      | Mem. management flaws | Y |
| 4      | buffer overflow | Y |
| 5      | TOCTTOU | Y |
| 6      | type misuses | N |
| 7      | reference counting errors | N |
| 8      | integer overflow | Y |
| 9      | GIL flaws | N |
| 10     | API evolution | Y |

## Full list of bugs

Prefix of all the paths below is Pillow/src/ (Pillow 5.4.1).

Our description will be in the following format:

```
path, line numbers
(similar ones)
code excerpt
```

### mishandling exceptions

encode.c, 1063-1068

```C
if (context->tile_offset_x <= context->offset_x - context->tile_size_x
    || context->tile_offset_y <= context->offset_y - context->tile_size_y) {
    PyErr_SetString(PyExc_ValueError,
                    "JPEG 2000 tile offset too small; top left tile must "
                    "intersect image area");
}
```

### insufficient error checking

_imaging.c, 2004-2007

```C
PyObject* item = Py_BuildValue(
    "iN", v->count, getpixel(self->image, self->access, v->x, v->y)
    );
PyList_SetItem(out, i, item);
```

```PyList_SetItem``` does not perform empty checking on ```item``` at all.

_imaging.c, 3507
_imaging.c, 3509
_imaging.c, 3511
_imaging.c, 3513
_imaging.c, 3515
_imaging.c, 3517
_imaging.c, 3843
_imaging.c, 3850
_imaging.c, 3869
_imaging.c, 3876
_imaging.c, 3880
_imagingmorph.c, 263
_imagingft.c, 952
_imagingft.c, 957
imagingcms.c, 1594

```C
PyDict_SetItemString(d, "new_count",
                     PyInt_FromLong(arena->stats_new_count));
```

```PyDict_SetItemString``` checks empty using assertion.

### Mem. management flaws

libImaging/Resample.c, 613-627

```C
ksize_horiz = precompute_coeffs(imIn->xsize, box[0], box[2], xsize,
                                filterp, &bounds_horiz, &kk_horiz);
if ( ! ksize_horiz) {
    return NULL;
}

ksize_vert = precompute_coeffs(imIn->ysize, box[1], box[3], ysize,
                                filterp, &bounds_vert, &kk_vert);
if ( ! ksize_vert) {
    free(bounds_horiz);
    free(kk_horiz);
    free(bounds_vert);
    free(kk_vert);
    return NULL;
}
```

### integer overflow

encode.c, 997

```C
if (!PyArg_ParseTuple(args, "ss|OOOsOIOOOssi", &mode, &format,
                        &offset, &tile_offset, &tile_size,
                        &quality_mode, &quality_layers, &num_resolutions,
                        &cblk_size, &precinct_size,
                        &irreversible, &progression, &cinema_mode,
                        &fd))
    return NULL;
```

### API evolution

encode.c, 179, 181 (2 errors in one format string)
encode.c, 126
encode.c, 228 (4)
encode.c, 407, 408
encode.c, 443
encode.c, 473, 474
encode.c, 506
encode.c, 564, 565, 566, 568
encode.c, 704-710, 713, 715, 717
encode.c, 988, 995

```C
int fh;
int bufsize = 16384;

if (!PyArg_ParseTuple(args, "i|i", &fh, &bufsize))
    return NULL;
```
