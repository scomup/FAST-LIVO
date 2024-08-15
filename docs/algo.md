
### Proof dImg

### Bilinear Interpolation
Bilinear interpolation is used to estimate the intensity value at a sub-pixel location \((u, v)\) based on the intensities of the four nearest pixels:

- **Top-left** pixel: \( I(u_0, v_0) \)
- **Top-right** pixel: \( I(u_1, v_0) \)
- **Bottom-left** pixel: \( I(u_0, v_1) \)
- **Bottom-right** pixel: \( I(u_0, v_1) \)

Here:
- \( u_0 \) and \( u_1 \) are the integer coordinates immediately to the left and right of \( u \).
- \( v_0 \) and \( v_1 \) are the integer coordinates immediately above and below \( v \).

The interpolated intensity at \((u, v)\) is given by:

\[
I(u, v) = (1 - \alpha)(1 - \beta) I(u_0, v_0) + \alpha(1 - \beta) I(u_1, v_0) + (1 - \alpha)\beta I(u_0, v_1) + \alpha\beta I(u_1, v_1)
\]

Where:
- \( \alpha = u - u_0 \)
- \( \beta = v - v_0 \)

### Finite Difference Approximation
To compute the horizontal derivative \( du \), we approximate it using finite differences:

\[
\frac{\partial I(u, v)}{\partial u} \approx \frac{I(u+\Delta u, v) - I(u-\Delta u, v)}{2\Delta u}
\]

If \( \Delta u = 1 \), this simplifies to:

\[
\frac{\partial I(u, v)}{\partial u} \approx \frac{I(u+1, v) - I(u-1, v)}{2}
\]

### Applying Bilinear Interpolation to Derivatives
Now, let's apply bilinear interpolation to the finite difference approximation:

#### Compute \( I(u+1, v) \):
For the point \( (u+1, v) \), the bilinear interpolation involves the following four pixel values:
- \( I(u_1, v_0) \)
- \( I(u_2, v_0) \)
- \( I(u_1, v_1) \)
- \( I(u_2, v_1) \)

The interpolated intensity is:

\[
I(u+1, v) \approx (1 - \alpha)(1 - \beta) I(u_1, v_0) + \alpha(1 - \beta) I(u_2, v_0) + (1 - \alpha)\beta I(u_1, v_1) + \alpha\beta I(u_2, v_1)
\]

#### Compute \( I(u-1, v) \):

Similary:

\[
I(u-1, v) \approx (1 - \alpha)(1 - \beta) I(u_{-1}, v_0) + \alpha(1 - \beta) I(u_0, v_0) + (1 - \alpha)\beta I(u_{-1}, v_1) + \alpha\beta I(u_0, v_1)
\]

### Derivative Calculation
Now, using these expressions, we can compute \( du \):

\[
du = 0.5 \times \left(I(u+1, v) - I(u-1, v)\right)
\]


```cpp
const float w_ref_tl = (1.0-subpix_u_ref) * (1.0-subpix_v_ref); // (1-alpha)(1-beta)
const float w_ref_tr = subpix_u_ref * (1.0-subpix_v_ref); // alpha(1-beta)
const float w_ref_bl = (1.0-subpix_u_ref) * subpix_v_ref; // (1-alpha)beta
const float w_ref_br = subpix_u_ref * subpix_v_ref; // alpha * beta


float du = 0.5f * ((w_ref_tl * img_ptr[scale * width * 0 + scale * 1] +  // I(u_1, v_0)
                    w_ref_tr * img_ptr[scale * width * 0 + scale * 2] +  // I(u_2, v_0)
                    w_ref_bl * img_ptr[scale * width * 1 + scale * 1] + // I(u_1, v_1)
                    w_ref_br * img_ptr[scale * width * 1 + scale * 2]) -  // I(u_2, v_1)
                   (w_ref_tl * img_ptr[scale * width * 0 + scale * (-1)] + // I(u_-1, v_0)
                    w_ref_tr * img_ptr[scale * width * 0 + scale * 0] +  // I(u_0, v_0)
                    w_ref_bl * img_ptr[scale * width * 1 + scale * (-1)] + // I(u_-1, v_1)
                    w_ref_br * img_ptr[scale * width * 1 + scale * 0])); // I(u_0, v_1)

```

dv
\[
dv = 0.5 \times \left(I(u, v+1) - I(u, v-1)\right)
\]

\[
I(u, v+1) \approx (1 - \alpha)(1 - \beta) I(u_0, v_1) + \alpha(1 - \beta) I(u_0, v_2) + (1 - \alpha)\beta I(u_1, v_1) + \alpha\beta I(u_1, v_2)
\]

\[
I(u, v-1) \approx (1 - \alpha)(1 - \beta) I(u_{0}, v_{-1}) + \alpha(1 - \beta) I(u_0, v_0) + (1 - \alpha)\beta I(u_{1}, v_{-1}) + \alpha\beta I(u_1, v_0)
\]

```cpp
float dv = 0.5f * ((w_ref_tl * img_ptr[scale * width *   1 + scale * 0] + 
                    w_ref_tr * img_ptr[scale * width *   1 + scale * 1] + 
                    w_ref_bl * img_ptr[scale * width *   2 + scale * 0] + 
                    w_ref_br * img_ptr[scale * width *   2 + scale * 1]) - 
                   (w_ref_tl * img_ptr[scale * width *(-1) + scale * 0] + 
                    w_ref_tr * img_ptr[scale * width *(-1) + scale * 1] + 
                    w_ref_bl * img_ptr[scale * width *   0 + scale * 0] +
                    w_ref_br * img_ptr[scale * width *   0 + scale * 1]));

```