
print('//-----CensoObjetivo------//')
IF OBJECT_ID('tempdb..#GruposBarcos') IS NOT NULL DROP TABLE #GruposBarcos
SELECT * INTO #GruposBarcos FROM SGP_SIPE.fenix.BuqueGrupo WHERE id in (2596)

print('//-----BuquesxCensoObjetivo------//')
IF OBJECT_ID('tempdb..#BuquesxCensoObjetivo') IS NOT NULL DROP TABLE #BuquesxCensoObjetivo
SELECT BXBG.Id
	,BXBG.IdBuque
	,BXBG.IdBuqueGrupo
	,BXBG.FcEfectoInicial
	,BXBG.FcEfectoFinal
	,GB.Descripcion Grupo
INTO #BuquesxCensoObjetivo
FROM SGP_SIPE.fenix.BuquexBuqueGrupo BXBG
	INNER JOIN #GruposBarcos GB ON BXBG.IdBuqueGrupo=GB.Id
WHERE CONVERT(DATE,BXBG.FcEfectoFinal)>=CONVERT(DATE,'01/01/2021')

print('//-----BuquesActivosxCensoObjetivo------//')
IF OBJECT_ID('tempdb..#BuquesActivosxCensoObjetivo') IS NOT NULL DROP TABLE #BuquesActivosxCensoObjetivo
SELECT DISTINCT A.IDBUQUE,IDLOCALIZADOR
INTO #BuquesActivosxCensoObjetivo
FROM
	(SELECT BXG.*
		,B.IdLocalizador
		,B.CFR
		,B.Nombre
	FROM #BuquesxCensoObjetivo BXG
		LEFT JOIN SGP_SIPE.fenix.Buque B ON  BXG.IdBuque=B.Id
	)A

print('//-----Posiciones------//')
IF OBJECT_ID('tempdb..#Posiciones') IS NOT NULL DROP TABLE #Posiciones
SELECT B.*
	,P.Id IdPosicion
	,P.FcIval
	,P.FcFval
	,P.Geom
	,P.Rumbo
	,P.Velocidad
	,P.Suceso
	,P.IdZonaPortuaria
	,Latitud=P.Geom.STY
	,Longitud=P.Geom.STX
	,Año=YEAR(P.FcIVal)
	,Mes=MONTH(P.FcIval)
INTO #Posiciones
FROM #BuquesActivosxCensoObjetivo B
	INNER JOIN SGP_SIPE_EXPLOTACION.CSP.PosicionCompletaMASTER2 P ON B.IdLocalizador=P.IdLocalizador
	INNER JOIN xea.Diario D ON D.IdBuque = B.IdBuque
									AND convert(date, P.FcIval) BETWEEN convert(date, D.FcSalida) AND convert(date, D.FcRegreso)
WHERE P.Valida=1
	AND P.Suceso IN (0,9)
	AND P.IdZonaPortuaria IS NULL
	AND D.Id = '1757628'

SELECT * FROM #Posiciones order by FcIval asc

