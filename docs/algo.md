Residual error
$$
r(R_{wi}, t_{wi}, \cdots) = I(\mathbf{u}(p_c(R_{cw}(R_{wi}, R_{ci}), t_{cw}(R_{wi}, R_{ci}, t_{wi}, t_{ci}), p_w))) - q
$$

$$
R_{cw} = R_{ci} R_{wi}^T
$$

$$
t_{cw} = -R_{ci} R_{wi}^T t_{wi} + t_{ci}
$$

### dr_dRwi

$$
\newcommand{\diff}[2]{\frac{\partial #1}{\partial #2}} %diff
$$


$$
\diff{r}{R_{wi}} = \diff{r}{I} \diff{I}{u} \diff{u}{p_c} \diff{p_c}{R_{cw}} \diff{R_{cw}}{R_{wi}} + 
\diff{r}{I} \diff{I}{u} \diff{u}{p_c} \diff{p_c}{t_{cw}} \diff{t_{cw}}{R_{wi}}
$$

```cpp
                    Jdphi = dr_du * du_dpc * dpc_dRcw;
                    Jdp = -dr_du * du_dpc;
                    JdR = dr_du * du_dpc * dpc_dRcw * JRcw_dRiw + 
                          dr_du * du_dpc * Jdp_dR;
                    Jdt = Jdp * Jdp_dt;
```

### dr_du (Jimg)

dr_du(Jimg) is the Jacobian matrix representing the derivative of the residual error with respect to the image coordinates $\mathbf{u}$.

$$
\diff{r}{\mathbf{u} } = \left[  \diff{r}{u}, \diff{r}{v} \right]
$$

where:
$\mathbf{u} = \left[ u, v \right]^T$

$$
I(u, v) = (1 - \alpha)(1 - \beta) I(u_0, v_0) + \alpha(1 - \beta) I(u_1, v_0) + (1 - \alpha)\beta I(u_0, v_1) + \alpha\beta I(u_1, v_1)
$$

### Bilinear Interpolation
Bilinear interpolation is used to estimate the intensity value at a sub-pixel location $(u, v)$ based on the intensities of the four nearest pixels:

- **Top-left** pixel: $ I(u_0, v_0) $
- **Top-right** pixel: $ I(u_1, v_0) $
- **Bottom-left** pixel: $ I(u_0, v_1) $
- **Bottom-right** pixel: $ I(u_0, v_1) $

Here:
- $ u_0 $ and $ u_1 $ are the integer coordinates immediately to the left and right of $ u $.
- $ v_0 $ and $ v_1 $ are the integer coordinates immediately above and below $ v $.

The interpolated intensity at $(u, v)$ is given by:

$$
I(u, v) = (1 - \alpha)(1 - \beta) I(u_0, v_0) + \alpha(1 - \beta) I(u_1, v_0) + (1 - \alpha)\beta I(u_0, v_1) + \alpha\beta I(u_1, v_1)
$$

Where:
- $ \alpha = u - u_0 $
- $ \beta = v - v_0 $

### Finite Difference Approximation
To compute the horizontal derivative $ du $, we approximate it using finite differences:

$$
\frac{\partial I(u, v)}{\partial u} \approx \frac{I(u+\Delta u, v) - I(u-\Delta u, v)}{2\Delta u}
$$

If $ \Delta u = 1 $, this simplifies to:

$$
\frac{\partial I(u, v)}{\partial u} \approx \frac{I(u+1, v) - I(u-1, v)}{2}
$$

### Applying Bilinear Interpolation to Derivatives
Now, let's apply bilinear interpolation to the finite difference approximation:

#### Compute $ I(u+1, v) $:
For the point $ (u+1, v) $, the bilinear interpolation involves the following four pixel values:
- $ I(u_1, v_0) $
- $ I(u_2, v_0) $
- $ I(u_1, v_1) $
- $ I(u_2, v_1) $

The interpolated intensity is:

$$
I(u+1, v) \approx (1 - \alpha)(1 - \beta) I(u_1, v_0) + \alpha(1 - \beta) I(u_2, v_0) + (1 - \alpha)\beta I(u_1, v_1) + \alpha\beta I(u_2, v_1)
$$

#### Compute $ I(u-1, v) $:

Similary:

$$
I(u-1, v) \approx (1 - \alpha)(1 - \beta) I(u_{-1}, v_0) + \alpha(1 - \beta) I(u_0, v_0) + (1 - \alpha)\beta I(u_{-1}, v_1) + \alpha\beta I(u_0, v_1)
$$

### Derivative Calculation
Now, using these expressions, we can compute $ du $:

$$
du = 0.5 \times \left(I(u+1, v) - I(u-1, v)\right)
$$


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
$$
dv = 0.5 \times \left(I(u, v+1) - I(u, v-1)\right)
$$

$$
I(u, v+1) \approx (1 - \alpha)(1 - \beta) I(u_0, v_1) + \alpha(1 - \beta) I(u_1, v_1) + (1 - \alpha)\beta I(u_0, v_2) + \alpha\beta I(u_1, v_2)
$$

$$
I(u, v-1) \approx (1 - \alpha)(1 - \beta) I(u_{0}, v_{-1}) + \alpha(1 - \beta) I(u_1, v_{-1}) + (1 - \alpha)\beta I(u_{0}, v_{0}) + \alpha\beta I(u_1, v_0)
$$

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

### du_dpc (Jdpi)


$$
\begin{aligned}
\mathbf{u}(p_c) 
&=
\begin{bmatrix} x f_x /z + c_x \\ y f_y /z + c_y \end{bmatrix} 
\end{aligned}
$$

$$
\begin{aligned}
\diff{\mathbf{u}}{p_c}
&= 
\begin{bmatrix} 
f_x/z & 0 & -f_x x/z^2 \\ 
0 & f_y/z & -f_y y/z^2
\end{bmatrix}  \\
\end{aligned}
$$

where:
$p_c = [x, y, z]^T$

### dpc_dRcw (p_hat)

$$
p_c = R_{cw} p_w + t_{cw}
$$

$$
\newcommand{\skew}[1]{[{#1}]_{\times}} %skew matrix
$$

$$
\diff{p_c}{R_{cw}} = -R_{cw} \skew{p_{w}}
$$


xci = np.array([0.1, 0.3, 0.5, 0.1, 0.2, 0.3])
xwi = np.array([-0.1, 0.1, -0.2, -0.3, 0.1, 0.1])

xiw, dxiw_dxwi = pose_inv(xwi, calcJ=True)
xcw, _, dxcw_dxiw = pose_plus(xci, xiw, True)



dxcw_dxwi = dxcw_dxiw @ dxiw_dxwi
