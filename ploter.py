import wx
import control
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from warnings import filterwarnings

filterwarnings("ignore", category=FutureWarning)

class BodePlotFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(BodePlotFrame, self).__init__(*args, **kw)
        self.SetSize((800, 600))
        self.Centre()
        self.SetTitle("Plotador de Diagrama de Bode")

        # Painel principal
        main_panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        input_box = wx.BoxSizer(wx.HORIZONTAL)

        self.num = wx.TextCtrl(main_panel, value="1 2")
        self.den = wx.TextCtrl(main_panel, value="1 3 2")
        plot_btn = wx.Button(main_panel, label="Plotar")

        input_box.Add(wx.StaticText(main_panel, label="Numerador:"), 0, wx.ALL | wx.CENTER, 5)
        input_box.Add(self.num, 1, wx.ALL | wx.EXPAND, 5)
        input_box.Add(wx.StaticText(main_panel, label="Denominador:"), 0, wx.ALL | wx.CENTER, 5)
        input_box.Add(self.den, 1, wx.ALL | wx.EXPAND, 5)
        input_box.Add(plot_btn, 0, wx.ALL | wx.CENTER, 5)

        vbox.Add(input_box, 0, wx.EXPAND | wx.ALL, 5)

        self.figure, self.axes = plt.subplots(2, 1, figsize=(6, 4))
        self.canvas = FigureCanvas(main_panel, -1, self.figure)

        vbox.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 5)

        main_panel.SetSizer(vbox)

        plot_btn.Bind(wx.EVT_BUTTON, self.on_plot)

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_plot(self, event):
        try:
            num = [float(x) for x in self.num.GetValue().split()]
            den = [float(x) for x in self.den.GetValue().split()]

            sistema = control.TransferFunction(num, den)
            print("\nFunção de transferência:")
            sistema_to_str = str(sistema).split('\n')
            print(sistema_to_str[4]) # no índice 4 começa a função
            print(sistema_to_str[5])
            print(sistema_to_str[6])

            self.figure.clear()

            mag_ax, phase_ax = self.figure.subplots(2, 1)

            control.bode_plot(sistema, dB=True, Hz=False, deg=True, plot=True, ax=[mag_ax, phase_ax])

            mag_ax.set_title("Diagrama de Bode (Magnitude e Fase)")
            mag_ax.grid(True, which="both")
            phase_ax.grid(True, which="both")

            self.canvas.draw()

        except Exception as e:
            wx.MessageBox(f"Erro ao processar: {e}", "Erro", wx.ICON_ERROR)

    def on_close(self, event):
        self.canvas.Close()
        self.Close()

def main():
    app = wx.App(False)
    frame = BodePlotFrame(None)
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()