| |  | |
| -------- | ------- | ------- |
| $u_1$ $v_1$  | $u_2$ $v_1$    | $u_3$ $v_1$    |
| $u_1$ $v_2$  | $u_2$ $v_2$    | $u_3$ $v_2$    |
| $u_1$ $v_3$  | $u_2$ $v_3$    | $u_3$ $v_3$    |



### Step 1: Bilinear Interpolation
In image processing, bilinear interpolation is used to estimate the intensity value at a sub-pixel location \((u, v)\) based on the intensities of the four nearest pixels:

- **Top-left** pixel: \( I(u_1, v_1) \)
- **Top-right** pixel: \( I(u_2, v_1) \)
- **Bottom-left** pixel: \( I(u_1, v_2) \)
- **Bottom-right** pixel: \( I(u_2, v_2) \)

Here:
- \( u_1 \) and \( u_2 \) are the integer coordinates immediately to the left and right of \( u \).
- \( v_1 \) and \( v_2 \) are the integer coordinates immediately above and below \( v \).

The interpolated intensity at \((u, v)\) is given by:

\[
I(u, v) = (1 - \alpha)(1 - \beta) I(u_1, v_1) + \alpha(1 - \beta) I(u_2, v_1) + (1 - \alpha)\beta I(u_1, v_2) + \alpha\beta I(u_2, v_2)
\]

Where:
- \( \alpha = u - u_1 \)
- \( \beta = v - v_1 \)

### Step 2: Finite Difference Approximation
To compute the horizontal derivative \( du \), we approximate it using finite differences:

\[
\frac{\partial I(u, v)}{\partial u} \approx \frac{I(u+\Delta u, v) - I(u-\Delta u, v)}{2\Delta u}
\]

If \( \Delta u = 1 \), this simplifies to:

\[
\frac{\partial I(u, v)}{\partial u} \approx \frac{I(u+1, v) - I(u-1, v)}{2}
\]

### Step 3: Applying Bilinear Interpolation to Derivatives
Now, let's apply bilinear interpolation to the finite difference approximation:

#### Compute \( I(u+1, v) \):
For the point \( (u+1, v) \), the bilinear interpolation involves the following four pixel values:
- \( I(u_2, v_1) \)
- \( I(u_3, v_1) \)
- \( I(u_2, v_2) \)
- \( I(u_3, v_2) \)

The interpolated intensity is:

\[
I(u+1, v) \approx (1 - \alpha)(1 - \beta) I(u_2, v_1) + \alpha(1 - \beta) I(u_3, v_1) + (1 - \alpha)\beta I(u_2, v_2) + \alpha\beta I(u_3, v_2)
\]

#### Compute \( I(u-1, v) \):
For the point \( (u-1, v) \), we use:
- \( I(u_0, v_1) \)
- \( I(u_1, v_1) \)
- \( I(u_0, v_2) \)
- \( I(u_1, v_2) \)

The interpolated intensity is:

\[
I(u-1, v) \approx (1 - \alpha)(1 - \beta) I(u_0, v_1) + \alpha(1 - \beta) I(u_1, v_1) + (1 - \alpha)\beta I(u_0, v_2) + \alpha\beta I(u_1, v_2)
\]

### Step 4: Derivative Calculation
Now, using these expressions, we can compute \( du \):

\[
du = 0.5 \times \left(I(u+1, v) - I(u-1, v)\right)
\]

Expanding this:

\[
du \approx 0.5 \times \left[
\begin{aligned}
&((1 - \alpha)(1 - \beta) I(u_2, v_1) + \alpha(1 - \beta) I(u_3, v_1) + (1 - \alpha)\beta I(u_2, v_2) + \alpha\beta I(u_3, v_2)) \\
&- ((1 - \alpha)(1 - \beta) I(u_0, v_1) + \alpha(1 - \beta) I(u_1, v_1) + (1 - \alpha)\beta I(u_0, v_2) + \alpha\beta I(u_1, v_2))
\end{aligned}
\right]
\]

However, in practical implementations, we focus on the contributions from the immediate neighbors, which leads to the simplified form of the derivative:

\[
du \approx 0.5 \times \left(I(u+1, v) - I(u-1, v)\right)
\]

### Conclusion
The formula you've provided:

\[
du = 0.5 \times \left(w\_ref\_tl \times \text{intensity at } (u+1, v) + w\_ref\_tr \times \text{intensity at } (u+2, v) + w\_ref\_bl \times \text{intensity at } (u+1, v+1) + w\_ref\_br \times \text{intensity at } (u+2, v+1)\right)
\]

is a way to combine bilinear interpolation with a finite difference approximation to estimate the image gradient \( du \). This expression focuses on interpolating the intensity at points slightly offset in the \( u \) direction, which aligns with the finite difference method for approximating derivatives.