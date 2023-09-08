

print('----Stocks-----')
IF OBJECT_ID('tempdb..#Stocks') IS NOT NULL DROP TABLE #Stocks
SELECT * INTO #Stocks FROM tacn.Stocks WHERE Nombre IN ('ALB/AN05N','ALB/AS05N','BET/ATLANT','BSH/AN05N','BUM/ATLANT','SWO/AN05N','SWO/AS05N','SWO/MED','WHM/ATLANT','SAI/AE45W','SAI/AW45W'
				  ,'SMA/AN05N'--no esta declarado para el 2022
				  ,'YFT/ATLANT','BSH/AS05N','YFT/IOTC','SWO/F7120S','BET/F7120S','BET/IATTC') AND Campaña IN (2018, 2019, 2020, 2021, 2022) ORDER BY Nombre


print('----Cierres-----')
IF OBJECT_ID('tempdb..#Cierres') IS NOT NULL DROP TABLE #Cierres
SELECT * INTO #Cierres FROM SGP_SIPE.xeacierre.InfoBase WHERE ID in (21, 32, 43, 59, 66)


print('----BuquesxCenso-----')
IF OBJECT_ID('tempdb..#BuquesxCenso') IS NOT NULL DROP TABLE #BuquesxCenso
SELECT
	BxBG.IdBuque
	,BxBG.FcEfectoInicial
	,BxBG.FcEfectoFinal
	,CxM.Id as Idcenso
	,CxM.IdPesqueria
	,CxM.Descripcion as Censo 
	,P.Descripcion as Pesqueria
	,R.Descripcion as Region
INTO #BuquesxCenso
FROM SGP_SIPE.fenix.BuquexBuqueGrupo BxBG 
	INNER JOIN 	SGP_SIPE.fenix.CensoxModalidad CxM ON BxBG.IdBuqueGrupo = CxM.IdBuqueGrupo 
	INNER JOIN 	SGP_SIPE.fenix.Pesqueria P ON CxM.IdPesqueria = P.Id 
	INNER JOIN  SGP_SIPE.fenix.Region R ON P.IdRegion = R.Id

print('----Consumos-----')
IF OBJECT_ID('tempdb..#Consumos') IS NOT NULL DROP TABLE #Consumos
SELECT C.Id IdConsumo
	  ,C.IdDiario
	  ,C.FcSalida,C.FcCaptura,C.FcRegreso,C.FcDesembarque
	  ,Fecha=coalesce(FcCaptura,FcSalida,FcRegreso,FcDesembarque)
	  ,C.IdBuque
	  ,C.IdEspecie
	  ,C.IdDivision
	  ,C.PesoConsumo,C.PesoConsumoBajoTalla,PesoConsumoTotal=coalesce(C.PesoConsumo,0)+coalesce(C.PesoConsumoBajoTalla,0)
	  ,C.PesoCapturado,C.PesoCapturadoBajoTalla,PesoCapturadoTotal= coalesce(C.PesoCapturado,0)+coalesce(C.PesoCapturadoBajoTalla,0)
	  ,C.PesoDesembarcado,C.PesoDesembarcadoBajoTalla,PesoDesembarcadoTotal=coalesce(C.PesoDesembarcado,0)+coalesce(C.PesoDesembarcadoBajoTalla,0)
	  ,C.PesoDesembarcadoVivo,C.PesoDesembarcadoVivoBajoTalla,PesoDesembarcadoVivoTotal=coalesce(C.PesoDesembarcadoVivo,0)+coalesce(C.PesoDesembarcadoVivoBajoTalla,0)
	  ,C.PesoNotaVenta
	  ,C.PesoNotaVentaVivo
	  ,C.IdStock
	  ,S.Nombre Stock
	  ,CR.IdCierreXEA,CR.IdCierreTrazapes,C.IdInfoBase
INTO #Consumos
FROM SGP_SIPE.xeacierre.Consumo C
	INNER JOIN #Cierres CR ON C.IdInfoBase=CR.Id
	INNER JOIN #Stocks S ON C.IdStock=S.Id

print('----DetallesConsumos-----') -->(774819 rows affected)
IF OBJECT_ID('tempdb..#DetallesConsumos') IS NOT NULL DROP TABLE #DetallesConsumos
SELECT C.*
	  ,E.AL3
	  ,Especie=Coalesce(E.Nombre,E.Cientifico)
	  ,Zona=Z.Descripcion
	  ,BxC.Censo
	  ,BI.CFR
	  ,BI.Nombre NombreBuque
	  ,D.IdMareaOrigen Hoja
INTO #DetallesConsumos
FROM #Consumos C
	LEFT JOIN  SGP_SIPE.xeacierre.Diario D ON C.IdDiario  =D.Id AND C.IdBuque=D.IdBuque AND C.IdCierreXEA=D.IdCierre
	INNER JOIN SGP_SIPE.cat.Especie E      ON C.IdEspecie =E.Id
	INNER JOIN SGP_SIPE.fenix.Zona Z       ON C.IdDivision=Z.Id
	LEFT JOIN #BuquesxCenso BXC            ON C.IdBuque   =BXC.IdBuque
													AND CONVERT(DATE, C.Fecha) >= CONVERT(DATE, BXC.FcEfectoInicial)
													AND CONVERT(DATE, C.Fecha) <  CONVERT(DATE, BXC.FcEfectoFinal)
	LEFT JOIN SGP_SIPE.censo.BuqueIdentificacion BI ON C.IdBuque=BI.IdBuque
													AND CONVERT(DATE, C.Fecha) >= CONVERT(DATE, BI.FcEfectoInicial)
													AND CONVERT(DATE, C.Fecha) <  CONVERT(DATE, BI.FcEfectoFinal)

print('----ResumenConsumos-----') --> (69087 rows affected)
IF OBJECT_ID('tempdb..#ResumenConsumos') IS NOT NULL DROP TABLE #ResumenConsumos
SELECT 
	       Año = YEAR(FcCaptura)
		  ,Hoja
		  ,Zona
		  ,Censo
	      ,CFR
	      ,NombreBuque
	      ,Stock
	      ,AL3
	      ,Especie
	      ,PesoConsumoTotal			    =sum(PesoConsumoTotal)
	      ,PesoCapturadoTotal			=sum(PesoCapturadoTotal)
	      ,PesoDesembarcadoTotal		=sum(PesoDesembarcadoTotal)
	      ,PesoDesembarcadoVivoTotal	=sum(PesoDesembarcadoVivoTotal)
	      ,PesoNotaVenta				=sum(PesoNotaVenta)
	      ,PesoNotaVentaVivo			=sum(PesoNotaVentaVivo)

INTO #ResumenConsumos

FROM #DetallesConsumos

GROUP BY 
	YEAR(FcCaptura),
	Hoja
	,Zona
	,Censo
	,CFR
	,NombreBuque
	,Stock
	,AL3
	,Especie
ORDER BY Año ASC 

SELECT * FROM #ResumenConsumos