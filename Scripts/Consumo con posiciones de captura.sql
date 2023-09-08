print('//-----DatosRobbin------//')
IF OBJECT_ID('tempdb..#ConsumoDesagregado') IS NOT NULL DROP TABLE #ConsumoDesagregado
SELECT 
	 Cap.Posicion.STY Latitud
	,Cap.Posicion.STX Longitud
	,cast(C.FcCaptura as date) AS FcCaptura
	,HmCaptura = CONVERT(VARCHAR, DATEPART(HOUR,C.FcCaptura)) + ':' + CONVERT(VARCHAR, DATEPART(minute, C.FcCaptura))
	,BI.CFR
	,BI.Nombre NombreBuque
	,A.Codigo CodigoArte
	,A.IdArteUeAL3
	,sp.AL3 AS AL3
	,sp.Nombre NombreEspecie
	,sp.cientifico
	,Z.Descripcion AS Division
	,PesoConsumoTotal =	(PesoConsumo + PesoConsumoBajoTalla)

INTO #ConsumoDesagregado

FROM SGP_SIPE.xeaRes.Consumo C

	LEFT JOIN SGP_SIPE.xea.DesembarqueEspecie DE		ON C.IdDesembarqueEspecie = DE.Id
	LEFT JOIN SGP_SIPE.xea.Diario D						ON DE.IdDiario = D.Id
	
	LEFT JOIN SGP_SIPE.xea.CapturaEspecie CE			ON C.IdCapturaEspecie = CE.Id
	LEFT JOIN SGP_SIPE.xea.Captura Cap					ON CE.IdCaptura = Cap.Id

	INNER JOIN SGP_SIPE.cat.Especie sp					ON C.IdEspecie = sp.Id
	INNER JOIN SGP_SIPE.censo.BuqueIdentificacion BI	ON BI.IdBuque = C.IdBuque  AND C.FcSalida >= BI.FcEfectoInicial  AND C.FcSalida < BI.FcEfectoFinal
	LEFT JOIN SGP_SIPE.fenix.Arte A						ON C.IdArte = A.Id
	LEFT JOIN SGP_SIPE.fenix.Zona Z						ON C.IdDivision = Z.Id

WHERE YEAR(C.FcCaptura) in (2018, 2019, 2020, 2021, 2022, 2023) and
		Z.IdTipoZona < 2 and
		sp.al3 in ('ALB', 'BET', 'SKJ', 'SWO', 'YFT')




