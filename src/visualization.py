import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid GUI errors

import matplotlib.pyplot as plt
from PIL import Image
import textwrap
import os
import logging

logger = logging.getLogger(__name__)

def show_matched_images(style_names, image_paths, composition_desc):
    """
    Display the matched styles - saves to file instead of showing interactively

    Args:
      - style_names: a list of style names
      - image_paths: a list of image paths
      - composition_desc: a list of composition descriptions
    """
    try:
        # Skip visualization if no images
        if not image_paths or len(image_paths) == 0:
            logger.info("No images to display, skipping visualization")
            return
            
        # Display images in a grid (3 per row)
        fig, axes = plt.subplots(
            nrows=(len(image_paths) + 2) // 3,  # Calculate rows based on images
            ncols=3, 
            figsize=(15, 12)  # Adjust size for better spacing
        )

        # Flatten axes for easy iteration (handle case of single subplot)
        if len(image_paths) > 1:
            axes = axes.flatten()
        else:
            axes = [axes]

        # Plot each image
        for i, image_path in enumerate(image_paths):
            if i >= len(axes):
                break  # Avoid index errors
                
            try:
                img = Image.open(image_path)
                axes[i].imshow(img)
                axes[i].axis("off")
                axes[i].set_title(style_names[i] if i < len(style_names) else "", fontsize=10)
                
                desc = composition_desc[i] if i < len(composition_desc) else ""
                axes[i].text(
                    0.5,
                    -0.05, 
                    "\n".join(textwrap.wrap(desc, width=50)),
                    fontsize=8,
                    ha="center",
                    va="top",
                    transform=axes[i].transAxes
                )
            except Exception as e:
                logger.warning(f"Error displaying image {i}: {str(e)}")

        plt.tight_layout()
        
        # Save to file instead of showing interactively
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'matched_styles.png')
        fig.savefig(output_path)
        plt.close(fig)  # Close the figure to free memory
        
        logger.info(f"Visualization saved to {output_path}")
    except Exception as e:
        logger.error(f"Error in visualization: {str(e)}")
        # Don't raise exception, just log it to avoid crashing the application 