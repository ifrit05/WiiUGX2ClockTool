import customtkinter as ctk

# Init CTk theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def update_display(value):
    freq_mhz = float(value)
    gpu_clk_f = calculate_gpu_clk_f(freq_mhz)
    hex_val = f"0x{gpu_clk_f:X}"
    validated_freq = calculate_freq_from_gpu_clk_f(gpu_clk_f)

    output_var.set(hex_val)
    result_var.set(f"{validated_freq:.6f} MHz")

# Calculate gpu_clk_f funtion
def calculate_gpu_clk_f(freq_mhz):
    factor = (0 + 1) * (4 / 2)
    gpu_clk_f = (freq_mhz * factor / 27) * 65536
    return int(round(gpu_clk_f))

# Calculate freqMhz from gpu_clk_f
def calculate_freq_from_gpu_clk_f(gpu_clk_f):
    factor = (0 + 1) * (4 / 2)
    return 27 * (gpu_clk_f / 65536) / factor

# Copy gpu_clk_f hex value to clipboard 
def copy_to_clipboard():
    app.clipboard_clear()
    app.clipboard_append(output_var.get())
    show_copy_alert()
    
# Modify max slider values based on checkbox state
def unsafe_clocks_slider():
    if check_var.get() == 1:
        slider.configure(to=799.999775)
        clock_label.configure(text_color="red")
        slider.set(549.999775)
        update_display(slider.get())
    else:
        slider.configure(to=749.999775)
        clock_label.configure(text_color="green")
        slider.set(549.999775)
        update_display(slider.get())

def show_copy_alert():
    alert = ctk.CTkToplevel(app)
    alert.title("Copied!")
    alert.geometry("420x120")
    alert.resizable(False, False)
    alert.grab_set()
    
    frame_alert = ctk.CTkFrame(alert)
    frame_alert.pack(fill="x",
                     padx=20,
                     pady=(15, 5)
                    )

    ctk.CTkLabel(frame_alert,
                 text="I am not responsible for any damage caused by using this tool.",
                 font=("Helvetica", 12, "bold"),
                 text_color="red"
                ).pack(pady=(10, 10))

    ctk.CTkButton(alert,
                  text="OK",
                  corner_radius=4,
                  fg_color="red",
                  hover_color="darkred",
                  width=100,
                  command=alert.destroy
                 ).pack(pady=10,
                        padx=20,
                        anchor="e"
                       )

# GUI setup
app = ctk.CTk()
app.title("Wii U GX2 Clock Tool")
app.geometry("420x275")
app.resizable(False, False)

# Frame 1
frame_top = ctk.CTkFrame(app)
frame_top.pack(fill="x",
               padx=20,
               pady=(15, 5)
              )

ctk.CTkLabel(frame_top,
             text="GX2 Clock:",
             font=("Helvetica", 12, "bold")
            ).pack(pady=(10, 5),
                   padx=(10, 5),
                   anchor="w"
                  )

slider = ctk.CTkSlider(frame_top,
                       from_=549.999775,
                       to=749.999775,
                       number_of_steps=250,
                       command=update_display
                      )
slider.set(549.999775)
slider.pack(fill='x',
            padx=20
           )

result_var = ctk.StringVar()
clock_label = ctk.CTkLabel(frame_top,
                           textvariable=result_var,
                           font=("Helvetica", 24, "bold")
                          )
clock_label.configure(text_color="green")
clock_label.pack(pady=(10, 10))

# Frame 2
frame_bottom = ctk.CTkFrame(app)
frame_bottom.pack(fill="x",
                  padx=20,
                  pady=(5, 5)
                 )

output_var = ctk.StringVar()
ctk.CTkLabel(frame_bottom,
             text="gpu_clk_f:",
             font=("Helvetica", 12, "bold")
            ).pack(pady=(10, 5),
                   padx=(10, 5),
                   anchor="w"
                  )
ctk.CTkLabel(frame_bottom,
             textvariable=output_var,
             font=("Courier", 24, "bold")
            ).pack(pady=(0, 10))
            
check_var = ctk.IntVar()
checkbox = ctk.CTkCheckBox(app,
                           text="Enable Unsafe Clocks",
                           variable=check_var,
                           command=unsafe_clocks_slider
                          )
checkbox.pack(padx=20,
              pady=5,
              side=ctk.LEFT
             )
ctk.CTkButton(app,
              text="Copy",
              corner_radius=4,
              width=100,
              command=copy_to_clipboard
             ).pack(padx=20,
                    pady=5,
                    side=ctk.RIGHT,
                    anchor="e"
                   )

# Main
update_display(slider.get())
app.mainloop()
