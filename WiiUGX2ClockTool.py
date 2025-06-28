import customtkinter as ctk

# Init CTk theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def updateDisplay(value):
    freqMhz = float(value)
    gpu_clk_f = calcGpu_clk_f(freqMhz)
    hexVal = f"0x{gpu_clk_f:X}"
    validatedFreq = calcFreqFromGpu_clk_f(gpu_clk_f)
    clockLabelResultVar.set(hexVal)
    clockMhzLabelResultVar.set(f"{validatedFreq:.6f} MHz")

# Calculate gpu_clk_f funtion
def calcGpu_clk_f(freqMhz):
    factor = (0 + 1) * (4 / 2)
    gpu_clk_f = (freqMhz * factor / 27) * 65536
    return int(round(gpu_clk_f))

# Calculate freqMhz from gpu_clk_f
def calcFreqFromGpu_clk_f(gpu_clk_f):
    factor = (0 + 1) * (4 / 2)
    return 27 * (gpu_clk_f / 65536) / factor

# Copy gpu_clk_f hex value to clipboard 
def copyToClipboard():
    mainWindow.clipboard_clear()
    mainWindow.clipboard_append(clockLabelResultVar.get())
    showCopyAlertTopLevel()
    
# Modify max sliderMhz values based on unsafeClocksCheckBox state
def unsafeClocksSliderMhz():
    if unsafeClocksCheckBoxVar.get() == 1:
        sliderMhz.configure(to=799.999775)
        clockMhzLabel.configure(text_color="red")
        sliderMhz.set(549.999775)
        updateDisplay(sliderMhz.get())
    else:
        sliderMhz.configure(to=699.574837)
        clockMhzLabel.configure(text_color="green")
        sliderMhz.set(549.999775)
        updateDisplay(sliderMhz.get())

def showCopyAlertTopLevel():
    copyAlertTopLevel = ctk.CTkToplevel(mainWindow)
    copyAlertTopLevel.title("Copied!")
    copyAlertTopLevel.geometry("420x120")
    copyAlertTopLevel.resizable(False, False)
    copyAlertTopLevel.wait_visibility()
    copyAlertTopLevel.grab_set()
    
    frameCopyAlertTopLevel = ctk.CTkFrame(copyAlertTopLevel)
    frameCopyAlertTopLevel.pack(fill="x",
                     padx=20,
                     pady=(15, 5)
                    )

    ctk.CTkLabel(frameCopyAlertTopLevel,
                 text="I am not responsible for any damage caused by using this tool.",
                 font=("Helvetica", 12, "bold"),
                 text_color="red"
                ).pack(pady=(10, 10))

    ctk.CTkButton(copyAlertTopLevel,
                  text="OK",
                  corner_radius=4,
                  fg_color="red",
                  hover_color="darkred",
                  width=100,
                  command=copyAlertTopLevel.destroy
                 ).pack(pady=10,
                        padx=20,
                        anchor="e"
                       )

# GUI setup
mainWindow = ctk.CTk()
mainWindow.title("Wii U GX2 Clock Tool")
mainWindow.geometry("420x275")
mainWindow.resizable(False, False)

# Frame 1
frameTop = ctk.CTkFrame(mainWindow)
frameTop.pack(fill="x",
               padx=20,
               pady=(15, 5)
              )

ctk.CTkLabel(frameTop,
             text="GX2 Clock:",
             font=("Helvetica", 12, "bold")
            ).pack(pady=(10, 5),
                   padx=(10, 5),
                   anchor="w"
                  )

sliderMhz = ctk.CTkSlider(frameTop,
                       from_=549.999775,
                       to=699.574837,
                       number_of_steps=250,
                       command=updateDisplay
                      )
sliderMhz.set(549.999775)
sliderMhz.pack(fill='x',
            padx=20
           )

clockMhzLabelResultVar = ctk.StringVar()
clockMhzLabel = ctk.CTkLabel(frameTop,
                           textvariable=clockMhzLabelResultVar,
                           font=("Helvetica", 24, "bold")
                          )
clockMhzLabel.configure(text_color="green")
clockMhzLabel.pack(pady=(10, 10))

# Frame 2
frameBottom = ctk.CTkFrame(mainWindow)
frameBottom.pack(fill="x",
                  padx=20,
                  pady=(5, 5)
                 )

clockLabelResultVar = ctk.StringVar()
ctk.CTkLabel(frameBottom,
             text="gpu_clk_f:",
             font=("Helvetica", 12, "bold")
            ).pack(pady=(10, 5),
                   padx=(10, 5),
                   anchor="w"
                  )
ctk.CTkLabel(frameBottom,
             textvariable=clockLabelResultVar,
             font=("Courier", 24, "bold")
            ).pack(pady=(0, 10))
            
unsafeClocksCheckBoxVar = ctk.IntVar()
unsafeClocksCheckBox = ctk.CTkCheckBox(mainWindow,
                           text="Enable Unsafe Clocks",
                           variable=unsafeClocksCheckBoxVar,
                           command=unsafeClocksSliderMhz
                          )
unsafeClocksCheckBox.pack(padx=20,
              pady=5,
              side=ctk.LEFT
             )
ctk.CTkButton(mainWindow,
              text="Copy",
              corner_radius=4,
              width=100,
              command=copyToClipboard
             ).pack(padx=20,
                    pady=5,
                    side=ctk.RIGHT,
                    anchor="e"
                   )

# Main Loop
updateDisplay(sliderMhz.get())
mainWindow.mainloop()
