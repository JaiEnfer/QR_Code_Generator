import qrcode
from PIL import Image, ImageDraw, ImageFilter

def generate_qr_code_with_gradient(url, file_name, center_color=(255, 0, 0), outer_color=(0, 0, 255)):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Create a blank image with radial gradient fill
    gradient_img = Image.new('RGB', qr_img.size, (255, 255, 255))
    draw = ImageDraw.Draw(gradient_img)

    # Draw a radial gradient
    for y in range(gradient_img.height):
        for x in range(gradient_img.width):
            distance_to_center = ((x - gradient_img.width / 2) ** 2 + (y - gradient_img.height / 2) ** 2) ** 0.5
            color = tuple(int(center + (outer - center) * distance_to_center / (gradient_img.width / 2)) for center, outer in zip(center_color, outer_color))
            draw.point((x, y), fill=color)

    # Apply the QR code as a mask to the gradient image
    gradient_img = gradient_img.convert("L")
    qr_img = qr_img.convert("RGBA")

    # Ensure both images have the same size
    gradient_img = gradient_img.resize(qr_img.size, Image.ANTIALIAS)

    # Create a new image by combining the two images
    final_img = Image.new("RGBA", qr_img.size)
    final_img = Image.alpha_composite(final_img, qr_img)
    final_img = Image.alpha_composite(final_img, Image.merge('RGBA', (gradient_img, gradient_img, gradient_img, gradient_img)))

    # Save the final image to a file
    final_img.save(file_name)

if __name__ == "__main__":
    # Example usage
    website_url = "https://65574cfeb85f5.site123.me"
    output_file = "qrcode_with_gradient.png"

    generate_qr_code_with_gradient(website_url, output_file, center_color=(255, 0, 0), outer_color=(0, 0, 255))
    print(f"QR code with gradient generated and saved as {output_file}")

