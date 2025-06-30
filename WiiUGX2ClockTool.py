import customtkinter as ctk

ctk.set_appearance_mode("system")

# Constants
CLKXTAL_FREQ = 27
CLK_FACTOR = 2.0
CLK_SCALE = 65536
SAFE_MAX_FREQ = 699.574837
UNSAFE_MAX_FREQ = 799.999775
DEFAULT_FREQ = 549.999775

# Calculation Functions
def calc_gpu_clk_f(freq_mhz):
    gpu_clk_f = (freq_mhz * CLK_FACTOR / CLKXTAL_FREQ) * CLK_SCALE
    return int(round(gpu_clk_f))

def calc_freq_from_gpu_clk_f(gpu_clk_f):
    return CLKXTAL_FREQ * (gpu_clk_f / CLK_SCALE) / CLK_FACTOR

# UI Update Functions
def update_display(value):
    freq_mhz = float(value)
    gpu_clk_f = calc_gpu_clk_f(freq_mhz)
    hex_val = f"0x{gpu_clk_f:X}"
    validated_freq = calc_freq_from_gpu_clk_f(gpu_clk_f)
    clock_label_result_var.set(hex_val)
    clock_mhz_label_result_var.set(f"{validated_freq:.6f} MHz")

def unsafe_clocks_slider_mhz():
    if unsafe_clocks_checkbox_var.get() == 1:
        slider_mhz.configure(to=UNSAFE_MAX_FREQ)
        clock_mhz_label.configure(text_color="red")
        slider_mhz.set(DEFAULT_FREQ)
        update_display(slider_mhz.get())
    else:
        slider_mhz.configure(to=SAFE_MAX_FREQ)
        clock_mhz_label.configure(text_color="green")
        slider_mhz.set(DEFAULT_FREQ)
        update_display(slider_mhz.get())

# Event Handlers
def copy_to_clipboard():
    main_window.clipboard_clear()
    main_window.clipboard_append(clock_label_result_var.get())
    copy_button.configure(text="Copied!", fg_color="green", hover_color="darkgreen", state="disabled")
    main_window.after(1500, reset_copy_button)  # Reset button text after 3 seconds

def reset_copy_button():
    """Reset the copy button text after a delay."""
    copy_button.configure(text="Copy", fg_color=orig_copy_button_fg_color, hover_color=orig_copy_button_hover_color, state="normal")

# GUI Setup
main_window = ctk.CTk()
main_window.title("Wii U GX2 Clock Tool")
main_window.geometry("420x275")
main_window.resizable(False, False)

# Frame 1
frame_top = ctk.CTkFrame(main_window)
frame_top.pack(fill="x", padx=20, pady=(15, 5))

ctk.CTkLabel(
    frame_top,
    text="GX2 Clock:",
    font=("Helvetica", 12, "bold")
).pack(pady=(10, 5), padx=(10, 5), anchor="w")

slider_mhz = ctk.CTkSlider(
    frame_top,
    from_=DEFAULT_FREQ,
    to=SAFE_MAX_FREQ,
    number_of_steps=250,
    command=update_display
)
slider_mhz.set(DEFAULT_FREQ)
slider_mhz.pack(fill='x', padx=20)

clock_mhz_label_result_var = ctk.StringVar()
clock_mhz_label = ctk.CTkLabel(
    frame_top,
    textvariable=clock_mhz_label_result_var,
    font=("Helvetica", 24, "bold")
)
clock_mhz_label.configure(text_color="green")
clock_mhz_label.pack(pady=(10, 10))

# Frame 2
frame_bottom = ctk.CTkFrame(main_window)
frame_bottom.pack(fill="x", padx=20, pady=(5, 5))

clock_label_result_var = ctk.StringVar()
ctk.CTkLabel(
    frame_bottom,
    text="gpu_clk_f:",
    font=("Helvetica", 12, "bold")
).pack(pady=(10, 5), padx=(10, 5), anchor="w")
ctk.CTkLabel(
    frame_bottom,
    textvariable=clock_label_result_var,
    font=("Courier", 24, "bold")
).pack(pady=(0, 10))

unsafe_clocks_checkbox_var = ctk.IntVar()
unsafe_clocks_checkbox = ctk.CTkCheckBox(
    main_window,
    text="Enable Unsafe Clocks",
    font=("Helvetica", 12, "bold"),
    text_color="red",
    variable=unsafe_clocks_checkbox_var,
    command=unsafe_clocks_slider_mhz
)
unsafe_clocks_checkbox.pack(padx=20, pady=5, side=ctk.LEFT)

copy_button = ctk.CTkButton(
    main_window,
    text="Copy",
    corner_radius=4,
    width=100,
    command=copy_to_clipboard
)
copy_button.pack(padx=20, pady=5, side=ctk.RIGHT, anchor="e")
orig_copy_button_fg_color = copy_button.cget("fg_color")
orig_copy_button_hover_color = copy_button.cget("hover_color")

# Main Loop
update_display(slider_mhz.get())
main_window.mainloop()
