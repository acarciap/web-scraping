
import pandas as pd

year = 2014

r = SalarioMinimo('https://datosmacro.expansion.com')
dfSMI = r.getSMI(year, 'https://datosmacro.expansion.com/smi')

r = SalarioMedio('https://datosmacro.expansion.com/mercado-laboral')
dfSM = r.getSM(year, 'https://datosmacro.expansion.com/mercado-laboral/salario-medio')

r = PIB('https://datosmacro.expansion.com')
dfPIB = r.getPIB(year, 'https://datosmacro.expansion.com/pib')

dfAux = pd.merge( dfSMI, dfSM, on ='pais', how ='outer', suffixes=('_m', '_M'))
dfRsl = pd.merge( dfAux, dfPIB, on ='pais', how ='outer', suffixes=('_S', '_P'))

dfRsl = dfRsl.drop('anio_M',1)
dfRsl = dfRsl.drop('anio_m',1)

dfRsl.to_csv('myData')
	 