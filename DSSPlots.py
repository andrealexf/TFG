from dss import dss

dss.Plotting.enable()
dss.Text.Command = 'redirect IJAU11/Master_DU01_2022124950_IJAU11_--MBS-1--T--.dss'
#dss.Text.Command = 'redirect EPRITestCircuits/ckt5/Master_ckt5.dss'
#dss.ActiveCircuit.Solution.Solve()
''''''
#dss.Text.Command = 'set emergvminpu=0.1'
#dss.Text.Command = 'set normvminpu=1.03'

dss.Text.Command = 'plot scatter'

#dss.Text.Command = 'Plot type=zone object=teste  quantity=power max=2000'

#'redirect "D:\OpenDSS\EPRITestCircuits\ckt5\Master_ckt5.dss"'
#https://dss-extensions.org/DSS-Python/examples/Plotting.html?utm_source=chatgpt.com


