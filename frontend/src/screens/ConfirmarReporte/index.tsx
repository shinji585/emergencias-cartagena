
      import React, { useState } from 'react';
      import { View, Text, StyleSheet, TouchableOpacity, Alert, ActivityIndicator, ScrollView, Image } from 'react-native';
      import { OpciónEmergencia } from '../../constants/tiposEmergencia';
      import { crearReporte, obtenerDespacho } from '../../services/api/reportes';

      interface Props {
        opcion: OpciónEmergencia;
        datos: {
          lat: number;
          lng: number;
          fotoUrl: string | null;
          descripcion?: string | null;
          nombre: string;
          telefono: string;
        };
        onAtras: () => void;
        onExito: (reporteId: string) => void;
      }

      export const ConfirmarReporteScreen: React.FC<Props> = ({ opcion, datos, onAtras, onExito }) => {
        const [enviando, setEnviando] = useState(false);
        const [logs, setLogs] = useState<string[]>([]);
        const [mostrarLogs, setMostrarLogs] = useState(false);
        const [despacho, setDespacho] = useState<any | null>(null);

        const pushLog = (entry: any) => {
          try {
            const texto = typeof entry === 'string' ? entry : JSON.stringify(entry);
            setLogs(prev => [(new Date()).toISOString() + ' - ' + texto, ...prev].slice(0, 50));
          } catch (e) {
            setLogs(prev => [(new Date()).toISOString() + ' - ' + String(entry), ...prev].slice(0, 50));
          }
        };

        const handleEnviar = async () => {
          setEnviando(true);
          try {
            const payload = {
              tipo_emergencia: opcion.id,
              ubicacion_lat: datos.lat,
              ubicacion_lng: datos.lng,
              foto_url: datos.fotoUrl,
              descripcion: datos.descripcion ?? null,
              organismo: opcion.organismo,
              usuario_nombre: datos.nombre,
              usuario_telefono: datos.telefono,
            };

            console.debug('[UI] Enviando reporte payload:', payload);
            pushLog({ tipo: 'payload', payload });

            const respuesta = await crearReporte(payload);
            pushLog({ tipo: 'response', respuesta });

            // Obtener despacho calculado por backend (organismos a notificar, plan, etc.)
            try {
              const despachoResp = await obtenerDespacho(respuesta.id);
              pushLog({ tipo: 'despacho', despacho: despachoResp });
              console.debug('[UI] Despacho obtenido:', despachoResp);
              setDespacho(despachoResp);
            } catch (e) {
              pushLog({ tipo: 'despacho_error', error: (e as any)?.message || String(e) });
            }

            if (!respuesta || !respuesta.id) {
              console.warn('[UI] Respuesta inválida al crear reporte:', respuesta);
              Alert.alert('Error', 'La respuesta del servidor no es válida. Intenta nuevamente más tarde.');
              return;
            }

            Alert.alert(
              '🚨 Reporte Recibido',
              `Tu reporte ha sido enviado al equipo de ${opcion.organismo.toUpperCase()}.
      \n\nSeveridad clasificada por IA: ${respuesta.severidad?.toUpperCase() || 'DESCONOCIDA'}\nID: ${respuesta.id.slice(0, 8)}`,
              [{ text: 'Entendido', onPress: () => onExito(respuesta.id) }]
            );
          } catch (err: any) {
            console.error('[UI] Error al enviar reporte:', err);
            pushLog({ tipo: 'error', error: err?.message || String(err) });
            Alert.alert(
              'Atención',
              'No se pudo conectar con el servidor backend. Revisa que el backend en Docker esté activo.\n\nError: ' + (err?.message || String(err))
            );
          } finally {
            setEnviando(false);
          }
        };

        return (
          <View style={styles.container}>
            <TouchableOpacity style={styles.backBtn} onPress={onAtras} disabled={enviando}>
              <Text style={styles.backText}>← Modificar Datos</Text>
            </TouchableOpacity>

            <Text style={styles.title}>Confirmar Envío de Emergencia</Text>

            <View style={styles.summaryCard}>
              <Text style={styles.summaryTipo}>{opcion.titulo}</Text>
              <Text style={styles.summaryItem}>🏛️ Destino: <Text style={styles.bold}>{opcion.organismo.toUpperCase()}</Text></Text>
              <Text style={styles.summaryItem}>📍 GPS: {datos.lat.toFixed(5)}, {datos.lng.toFixed(5)}</Text>
              <Text style={styles.summaryItem}>👤 Reportante: {datos.nombre} ({datos.telefono})</Text>
              <Text style={styles.summaryItem}>📝 Descripción: {datos.descripcion ? datos.descripcion : 'No proporcionada'}</Text>
              {datos.fotoUrl ? (
                <Image source={{ uri: datos.fotoUrl }} style={styles.previewImage} />
              ) : (
                <Text style={styles.summaryItem}>📸 Foto adjunta: No</Text>
              )}
            </View>

            {/* Aviso legal explicito de trazabilidad exigido en seccion 1.4 */}
            <View style={styles.legalNotice}>
              <Text style={styles.legalTitle}>⚠️ AVISO LEGAL Y RESPONSABILIDAD</Text>
              <Text style={styles.legalBody}>
                Este reporte quedará registrado con tu ubicación GPS exacta, marca de tiempo e identidad ({datos.telefono}). 
                Las falsas alarmas o reportes mal intencionados constituyen un delito penado por la ley y serán remitidos a las autoridades competentes.
              </Text>
            </View>

            <TouchableOpacity
              style={[styles.sendBtn, { backgroundColor: opcion.color }, enviando && styles.disabledBtn]}
              onPress={handleEnviar}
              disabled={enviando}
            >
              {enviando ? (
                <ActivityIndicator color="#FFF" />
              ) : (
                <Text style={styles.sendBtnText}>ENVIAR REPORTE AHORA 🚨</Text>
              )}
            </TouchableOpacity>

            <View style={{ marginTop: 12 }}>
              <TouchableOpacity onPress={() => setMostrarLogs(s => !s)}>
                <Text style={{ color: '#94A3B8' }}>{mostrarLogs ? 'Ocultar logs' : 'Mostrar logs de envío'}</Text>
              </TouchableOpacity>
              {mostrarLogs && (
                <View style={styles.logBox}>
                  <ScrollView style={{ maxHeight: 200 }}>
                    {logs.length === 0 ? (
                      <Text style={styles.logText}>No hay logs aún.</Text>
                    ) : (
                      logs.map((l, i) => (
                        <Text key={i} style={styles.logText}>{l}</Text>
                      ))
                    )}
                  </ScrollView>
                </View>
              )}
            </View>

            {despacho && (
              <View style={styles.despachoBox}>
                <Text style={styles.despachoTitle}>🎯 Análisis Completado</Text>
                <Text style={styles.despachoLine}>Severidad: {despacho.severidad}</Text>
                {despacho.resumen_ia && <Text style={styles.despachoLine}>Resumen IA: {despacho.resumen_ia}</Text>}

                <Text style={[styles.despachoLine, { marginTop: 8, fontWeight: 'bold' }]}>📢 Organismos a despachar ({despacho.organismos_notificados?.length || 0}):</Text>
                {(despacho.organismos_notificados || []).map((org: any) => (
                  <View key={org.nombre} style={{ marginVertical: 4, paddingLeft: 8 }}>
                    <Text style={styles.despachoOrg}>• {org.nombre}</Text>
                    {org.telefono && <Text style={styles.despachoSmall}>📞 {org.telefono}</Text>}
                    {org.accion && <Text style={styles.despachoSmall}>✈️ {org.accion}</Text>}
                  </View>
                ))}

                {despacho.plan_candado && (
                  <View style={styles.planCandado}>
                    <Text style={{ fontWeight: 'bold', color: 'red' }}>🚔 PLAN CANDADO ACTIVADO</Text>
                    <Text>Radio: {despacho.plan_candado.radio_huida_km} km</Text>
                    <Text>Recomendación: {despacho.plan_candado.recomendacion_tactica}</Text>
                  </View>
                )}
              </View>
            )}
          </View>
        );
      };

      const styles = StyleSheet.create({
        container: {
          flex: 1,
          backgroundColor: '#0F172A',
          padding: 20,
        },
        backBtn: {
          marginTop: 10,
          marginBottom: 10,
        },
        backText: {
          color: '#38BDF8',
          fontSize: 14,
        },
        title: {
          fontSize: 20,
          fontWeight: 'bold',
          color: '#F8FAFC',
          marginBottom: 16,
        },
        summaryCard: {
          backgroundColor: '#1E293B',
          padding: 16,
          borderRadius: 12,
          marginBottom: 16,
        },
        summaryTipo: {
          color: '#38BDF8',
          fontSize: 18,
          fontWeight: 'bold',
          marginBottom: 10,
        },
        summaryItem: {
          color: '#CBD5E1',
          fontSize: 14,
          marginBottom: 6,
        },
        bold: {
          fontWeight: 'bold',
          color: '#F8FAFC',
        },
        legalNotice: {
          backgroundColor: '#451A03',
          borderColor: '#F59E0B',
          borderWidth: 1,
          padding: 14,
          borderRadius: 10,
          marginBottom: 20,
        },
        legalTitle: {
          color: '#F59E0B',
          fontWeight: 'bold',
          fontSize: 12,
          marginBottom: 4,
        },
        legalBody: {
          color: '#FEF3C7',
          fontSize: 11,
          lineHeight: 16,
        },
        sendBtn: {
          padding: 18,
          borderRadius: 12,
          alignItems: 'center',
          marginTop: 'auto',
        },
        disabledBtn: {
          opacity: 0.6,
        },
        sendBtnText: {
          color: '#FFFFFF',
          fontWeight: 'bold',
          fontSize: 18,
        },
        logBox: {
          backgroundColor: '#071022',
          borderColor: '#334155',
          borderWidth: 1,
          padding: 8,
          borderRadius: 8,
          marginTop: 8,
        },
        logText: {
          color: '#94A3B8',
          fontSize: 12,
          marginBottom: 6,
        },
        despachoBox: {
          backgroundColor: '#081223',
          borderColor: '#334155',
          borderWidth: 1,
          padding: 12,
          borderRadius: 8,
          marginTop: 14,
        },
        despachoTitle: {
          color: '#F8FAFC',
          fontWeight: 'bold',
          fontSize: 16,
          marginBottom: 6,
        },
        despachoLine: {
          color: '#CBD5E1',
          fontSize: 13,
          marginBottom: 4,
        },
        despachoOrg: {
          color: '#E2E8F0',
          fontSize: 13,
        },
        despachoSmall: {
          color: '#94A3B8',
          fontSize: 12,
          marginLeft: 6,
        },
        planCandado: {
          marginTop: 8,
          backgroundColor: '#2B0606',
          padding: 8,
          borderRadius: 6,
        },
        previewImage: {
          width: '100%',
          height: 180,
          borderRadius: 8,
          marginTop: 8,
        },
      });
