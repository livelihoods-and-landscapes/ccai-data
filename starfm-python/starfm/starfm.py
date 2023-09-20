import numpy as np
import os
import rasterio
import time


def spectral_difference(fine_t0_win, coarse_t0_win, r, c):
    """Compute spectral difference between fine and coarse resolution windows.

    Args:
        fine_t0_win (ndarray): window from fine resolution image.
        coarse_t0_win (ndarray): window from coarse resolution image.
        r (int): centre pixel row (0-axis) dimension.
        c (int): centre pixel column (1-axis) dimension.

    Returns:
        ndarray: flattened spectral difference between coarse and fine resolution windows.
        int / float: centre pixel value from spectral difference ndarray.
    """
    spec_diff = np.abs(fine_t0_win - coarse_t0_win)
    centre_spec_diff = spec_diff[r, c]

    spec_diff = np.ravel(spec_diff)

    return spec_diff, centre_spec_diff


def temporal_difference(coarse_t0_win, coarse_t1_win, r, c):
    """Compute temporal difference between coarse resolution windows.

    Args:
        coarse_t0_win (ndarray): window from coarse resolution image (t0).
        coarse_t1_win (ndarray): window from coarse resolution image (t1).
        r (int): centre pixel row (0-axis) dimension.
        c (int): centre pixel column (1-axis) dimension.

    Returns:
        ndarray: flattened temporal difference between coarse resolution windows.
        int / float: centre pixel value from temporal difference ndarray.
    """
    tmp_diff = np.abs(coarse_t1_win - coarse_t0_win)
    centre_tmp_diff = tmp_diff[r, c]

    tmp_diff = np.ravel(tmp_diff)

    return tmp_diff, centre_tmp_diff


def spatial_distance(window_size, spatial_impact_factor):
    """Compute spatial distance between all pixels in window and central pixel.

    Implementation based on Mileva et al. (2018): https://github.com/nmileva/starfm4py

    Args:
        window_size (int): dimensions of the window.
        spatial_impact_factor (int): from eqn (9) in Gao et al. (2006).
        A smaller value of gives the spatial distance a larger weighting relative to spectral and temporal distance.

    Returns:
        ndarray: flattened spatial distance for a window.
    """

    coord = np.sqrt((np.mgrid[0:window_size, 0:window_size] - window_size // 2) ** 2)
    spat_dist = np.sqrt(((0 - coord[0]) ** 2 + (0 - coord[1]) ** 2))

    rev_spat_dist = spat_dist / spatial_impact_factor + 1.0

    spat_dist = np.ravel(rev_spat_dist)

    return spat_dist


def get_spectral_threshold(fine_t0, n_classes):
    """Compute spectral similarity threshold.

    Args:
        fine_t0 (ndarray): full fine resolution scene at t0.
        n_classes (int): number of classes used to determine similar pixels.

    Returns:
        float: spectral similarity threshold used to identify spectrally similar neighbouring pixels within a window.
    """

    threshold = np.std(fine_t0) * 2 / n_classes

    return threshold


def get_spectral_and_sample_filtered(
    spectral_threshold,
    fine_t0_win,
    centre_pixel,
    centre_spec_diff,
    centre_tmp_diff,
    spec_diff,
    tmp_diff,
    tmp_diff_flag,
    mask,
    spectral_uncertainty,
    temporal_uncertainty,
):
    """Identify spectrally similar and high quality pixels within window to use for weight generation.

    In Gao et al. (2006) it is stated that eqn (15) and eqn (16) must be true for a pixel to be considered a weighting candidate.
    However, the USDA reference implementation R package ImageFusion use eqn (15) or eqn (16). Here, the stricter and is used.

    Following the R package ImageFusion, a flag is provided to indicate whether to use temporal weights. 

    Args:
        spectral_threshold (float): spectral similarity threshold used to identify spectrally similar neighbouring pixels within a window.
        fine_t0_win (ndarray): window from fine resolution image.
        centre_pixel (int /  float): centre pixel value from fine resolution image.
        centre_spec_diff (int / float): centre pixel value from spectral difference ndarray.
        centre_tmp_diff (int / float): centre pixel value from temporal difference ndarray.
        spec_diff (ndarray): flattened spectral difference between coarse and fine resolution windows.
        tmp_diff (ndarray): flattened temporal difference between coarse resolution windows.
        tmp_diff_flag (bool): boolean indicator whether to use temporal difference in weights.
        mask (bool): mask of valid and invalid pixels. Invalid pixels generally padding.
        spectral_uncertainty (int / float): uncertainty for spectral difference - eqn (15) Gao et al. (2006).
        temporal_uncertainty (int / float): uncertainty for temporal difference - eqn (16) Gao et al. (2006).

     Returns:
        ndarray: boolean values indicating valid pixels for weight generating within the window.
    """

    # get spectrally similar pixels in window
    fine_t0_win = np.ravel(fine_t0_win)
    window_similar = np.where(
        abs(centre_pixel - fine_t0_win) < spectral_threshold, 1, 0
    )

    # get high quality pixels in window
    spectral_filter = np.where(
        spec_diff < (centre_spec_diff + spectral_uncertainty), 1, 0
    )

    if tmp_diff_flag:
        tmp_filter = np.where(tmp_diff < (centre_tmp_diff + temporal_uncertainty), 1, 0)
        similar_and_filtered = window_similar * spectral_filter * tmp_filter
    else:
        similar_and_filtered = window_similar * spectral_filter

    # mask catches padded pixels at the edge of image
    mask = mask * 1

    # boolean mask of valid and not padded pixels
    similar_and_filtered = (similar_and_filtered * mask) == 1

    return similar_and_filtered


def get_weights(spec_diff, tmp_diff, tmp_diff_flag, spat_dist, similar_and_filtered):
    """Compute weights for pixels in window.

    Following the R package ImageFusion, a flag is provided to indicate whether to use temporal weights. 

    Args:
        spec_diff (ndarray): flattened spectral difference for a window.
        tmp_diff (ndarray): flattened temporal difference for a window.
        tmp_diff_flag (bool): boolean indicator whether to use temporal difference in weights.
        spat_dist (ndarray): flattened spatial distance for a window.
        similar_and_filtered (ndarray): boolean values indicating valid pixels for weight generating within the window.

    Returns:
        ndarray: weights for valid pixels within a window.
    """

    spec_dist = spec_diff + 1
    spec_dist = spec_dist[similar_and_filtered]

    spat_dist = spat_dist[similar_and_filtered]

    if tmp_diff_flag:
        tmp_dist = tmp_diff + 1
        tmp_dist = tmp_dist[similar_and_filtered]
        combined_weights = spec_dist * spat_dist * tmp_dist
    else:
        combined_weights = spec_dist * spat_dist

    combined_weights_reversed = 1 / combined_weights

    combined_weights_sum = np.sum(combined_weights_reversed)

    combined_and_normalised_weights = combined_weights_reversed / combined_weights_sum

    return combined_and_normalised_weights


def predict_weighted_fine(
    weights, fine_t0_win, coarse_t0_win, coarse_t1_win, similar_and_filtered
):
    """Predict fine t1 using weights in window.

    Args:
        weights (ndarray): weights for valid pixels within a window.
        fine_t0_win (_type_): window from fine resolution image at t0.
        coarse_t0_win (_type_): window from coarse resolution image at t0.
        coarse_t1_win (_type_): window from coarse resolution image at t1.
        similar_and_filtered (_type_): boolean values indicating valid pixels for weight generating within the window.

    Returns:
        int / float : prediction for centre pixel within window.
    """
    fine_t0_win = np.ravel(fine_t0_win)
    fine_t0_win = fine_t0_win[similar_and_filtered]

    coarse_t0_win = np.ravel(coarse_t0_win)
    coarse_t0_win = coarse_t0_win[similar_and_filtered]

    coarse_t1_win = np.ravel(coarse_t1_win)
    coarse_t1_win = coarse_t1_win[similar_and_filtered]

    fine_t1 = weights * ((coarse_t1_win + fine_t0_win) - coarse_t0_win)

    return np.sum(fine_t1)


def predict_unweighted_fine(fine_t0_ctr, coarse_t0_ctr, coarse_t1_ctr):
    """Local prediction for fine t1.

    Args:
        fine_t0_ctr (int / float): centre pixel in window from fine resolution image at t0.
        coarse_t0_ctr (int / float): centre pixel in window from coarse resolution image at t0.
        coarse_t1_ctr (int / float): centre pixel in window from coarse resolution image at t1.

    Returns:
        int / float: local fine resolution prediction at t1.
    """
    fine_t1 = (coarse_t1_ctr + fine_t0_ctr) - coarse_t0_ctr

    return np.sum(fine_t1)


def starfm(
    fine_t0,
    coarse_t0,
    coarse_t1,
    window_size,
    window_size_half,
    mask_val,
    dim_rows,
    dim_cols,
    tmp_diff_flag,
    spectral_uncertainty,
    temporal_uncertainty,
    spatial_impact_factor,
    n_classes
):
    """Predict fine t1 image using starfm.

    Following the R package ImageFusion, a flag is provided to indicate whether to use temporal weights. 

    Args:
        fine_t0 (ndarray): fine resolution image t0.
        coarse_t0 (ndarray): coarse resolution image t0.
        coarse_t1 (ndarray): coarse resolution image t1.
        window_size (int): window size (must be odd).
        window_size_half (int): half window size (floor) (e.g. is window size is 31 half window size is 15).
        mask_val (int): mask value for invalid pixels and padding on each of image.
        dim_rows (_type_): number of elements on rows (0-axis).
        dim_cols (_type_): number of elements on cols (1-axis).
        tmp_diff_flag (bool): boolean indicator whether to use temporal difference in weights.
        spectral_uncertainty (int / float): uncertainty for spectral difference - eqn (15) Gao et al. (2006).
        temporal_uncertainty (int / float): uncertainty for temporal difference - eqn (16) Gao et al. (2006).
        spatial_impact_factor (int): from eqn (9) in Gao et al. (2006). In pixel units.
        A smaller value of gives the spatial distance a larger weighting relative to spectral and temporal distance.
        n_classes (int): number of classes used to determine similar pixels.

    Returns:
        ndarray: starfm prediction for fine image at t1.
    """

    # compute spatial distance
    spat_dist = spatial_distance(window_size, spatial_impact_factor)

    # compute spectral similarity threshold
    spectral_threshold = get_spectral_threshold(fine_t0, n_classes)

    # array to hold predictions
    preds_arr = np.zeros(fine_t0.shape)

    # pad images with mask values
    fine_t0_pad = np.pad(
        fine_t0,
        ((window_size_half, window_size_half), (window_size_half, window_size_half)),
        constant_values=mask_val,
    )
    coarse_t0_pad = np.pad(
        coarse_t0,
        ((window_size_half, window_size_half), (window_size_half, window_size_half)),
        constant_values=mask_val,
    )
    coarse_t1_pad = np.pad(
        coarse_t1,
        ((window_size_half, window_size_half), (window_size_half, window_size_half)),
        constant_values=mask_val,
    )

    for r in range(0 + window_size_half, dim_rows + window_size_half):
        for c in range(0 + window_size_half, dim_cols + window_size_half):
            fine_t0_win = fine_t0_pad[
                r - window_size_half : r + window_size_half + 1,
                c - window_size_half : c + window_size_half + 1,
            ]
            coarse_t0_win = coarse_t0_pad[
                r - window_size_half : r + window_size_half + 1,
                c - window_size_half : c + window_size_half + 1,
            ]
            coarse_t1_win = coarse_t1_pad[
                r - window_size_half : r + window_size_half + 1,
                c - window_size_half : c + window_size_half + 1,
            ]

            mask = fine_t0_win != mask_val
            mask = np.ravel(mask)

            spec_diff, centre_spec_diff = spectral_difference(
                fine_t0_win, coarse_t0_win, window_size_half + 1, window_size_half + 1
            )
            tmp_diff, centre_tmp_diff = temporal_difference(
                coarse_t0_win, coarse_t1_win, window_size_half + 1, window_size_half + 1
            )

            centre_pixel_fine_t0 = fine_t0_win[window_size_half, window_size_half]
            centre_pixel_coarse_t0 = coarse_t0_win[window_size_half, window_size_half]
            centre_pixel_coarse_t1 = coarse_t1_win[window_size_half, window_size_half]

            similar_and_filtered = get_spectral_and_sample_filtered(
                spectral_threshold,
                fine_t0_win,
                centre_pixel_fine_t0,
                centre_spec_diff,
                centre_tmp_diff,
                spec_diff,
                tmp_diff,
                tmp_diff_flag,
                mask,
                spectral_uncertainty,
                temporal_uncertainty,
            )

            if np.sum(similar_and_filtered) > 0:
                weights = get_weights(
                    spec_diff, tmp_diff, tmp_diff_flag, spat_dist, similar_and_filtered
                )
                pred_fine_t1 = predict_weighted_fine(
                    weights,
                    fine_t0_win,
                    coarse_t0_win,
                    coarse_t1_win,
                    similar_and_filtered,
                )
            else:
                # local prediction if no valid pixels for weighting in window
                pred_fine_t1 = predict_unweighted_fine(
                    centre_pixel_fine_t0, centre_pixel_coarse_t0, centre_pixel_coarse_t1
                )

            preds_arr[r - window_size_half, c - window_size_half] = pred_fine_t1

    return preds_arr
