/**
 * Modal para mostrar el resultado de la solicitud
 */
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Alert,
  Divider,
  Paper,
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import type { SolicitudResponse } from '../types';

interface ResultModalProps {
  open: boolean;
  onClose: () => void;
  resultado: SolicitudResponse | null;
}

export default function ResultModal({ open, onClose, resultado }: ResultModalProps) {
  if (!resultado) return null;

  const esAprobado = resultado.estado === 'aprobado';

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {esAprobado ? (
            <CheckCircleIcon color="success" sx={{ fontSize: 40 }} />
          ) : (
            <CancelIcon color="error" sx={{ fontSize: 40 }} />
          )}
          <Typography variant="h5">
            Solicitud {esAprobado ? 'Pre-aprobada' : 'Rechazada'}
          </Typography>
        </Box>
      </DialogTitle>

      <DialogContent dividers>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          <Alert severity={esAprobado ? 'success' : 'error'}>
            {esAprobado
              ? '¡Felicidades! Su solicitud de crédito ha sido pre-aprobada.'
              : 'Lo sentimos, su solicitud de crédito no ha sido pre-aprobada.'}
          </Alert>

          {/* Información General */}
          <Box>
            <Typography variant="h6" gutterBottom color="primary">
              Información de la Solicitud
            </Typography>
            <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
              <Box>
                <Typography variant="subtitle2" color="text.secondary">
                  Número de Solicitud
                </Typography>
                <Typography variant="body1" fontWeight="bold">
                  #{resultado.id}
                </Typography>
              </Box>

              <Box>
                <Typography variant="subtitle2" color="text.secondary">
                  Sucursal
                </Typography>
                <Typography variant="body1">{resultado.sucursal_nombre}</Typography>
              </Box>

              <Box>
                <Typography variant="subtitle2" color="text.secondary">
                  Solicitante
                </Typography>
                <Typography variant="body1">{resultado.cliente_nombre}</Typography>
              </Box>

              <Box>
                <Typography variant="subtitle2" color="text.secondary">
                  Email
                </Typography>
                <Typography variant="body1">{resultado.cliente_email}</Typography>
              </Box>
            </Box>
          </Box>

          <Divider />

          {/* Información del Crédito */}
          <Box>
            <Typography variant="h6" gutterBottom color="primary">
              Detalles del Crédito
            </Typography>
            <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
              <Box>
                <Typography variant="subtitle2" color="text.secondary">
                  Monto Solicitado
                </Typography>
                <Typography variant="body1" fontWeight="bold">
                  ${resultado.monto_solicitado.toLocaleString('es-MX', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}
                </Typography>
              </Box>

              <Box>
                <Typography variant="subtitle2" color="text.secondary">
                  Plazo
                </Typography>
                <Typography variant="body1" fontWeight="bold">
                  {resultado.plazo_meses} meses
                </Typography>
              </Box>

              <Box>
                <Typography variant="subtitle2" color="text.secondary">
                  Ingreso Mensual
                </Typography>
                <Typography variant="body1">
                  ${resultado.ingreso_mensual.toLocaleString('es-MX', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}
                </Typography>
              </Box>

              <Box>
                <Typography variant="subtitle2" color="text.secondary">
                  Score Crediticio
                </Typography>
                <Typography variant="body1">{resultado.score_crediticio}</Typography>
              </Box>
            </Box>
          </Box>

          {/* Información Financiera (solo si es aprobado) */}
          {esAprobado && resultado.cuota_mensual && (
            <>
              <Divider />
              <Box>
                <Typography variant="h6" gutterBottom color="primary">
                  Plan de Pagos
                </Typography>
                <Paper sx={{ p: 2, bgcolor: 'success.50', border: '1px solid', borderColor: 'success.200' }}>
                  <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
                    <Box>
                      <Typography variant="subtitle2" color="text.secondary">
                        Cuota Mensual
                      </Typography>
                      <Typography variant="h6" color="success.dark" fontWeight="bold">
                        ${resultado.cuota_mensual.toLocaleString('es-MX', {
                          minimumFractionDigits: 2,
                          maximumFractionDigits: 2,
                        })}
                      </Typography>
                    </Box>

                    <Box>
                      <Typography variant="subtitle2" color="text.secondary">
                        Tasa de Interés Anual
                      </Typography>
                      <Typography variant="h6" color="success.dark" fontWeight="bold">
                        {resultado.tasa_interes_anual}%
                      </Typography>
                    </Box>

                    <Box>
                      <Typography variant="subtitle2" color="text.secondary">
                        Total de Intereses
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        ${resultado.total_intereses?.toLocaleString('es-MX', {
                          minimumFractionDigits: 2,
                          maximumFractionDigits: 2,
                        })}
                      </Typography>
                    </Box>

                    <Box>
                      <Typography variant="subtitle2" color="text.secondary">
                        Total a Pagar
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        ${resultado.total_a_pagar?.toLocaleString('es-MX', {
                          minimumFractionDigits: 2,
                          maximumFractionDigits: 2,
                        })}
                      </Typography>
                    </Box>
                  </Box>
                </Paper>
              </Box>
            </>
          )}

          {/* Motivo de Rechazo */}
          {!esAprobado && resultado.motivo_rechazo && (
            <>
              <Divider />
              <Box>
                <Typography variant="h6" gutterBottom color="error">
                  Motivo del Rechazo
                </Typography>
                <Alert severity="warning">{resultado.motivo_rechazo}</Alert>
              </Box>
            </>
          )}

          {/* Información adicional */}
          {esAprobado && (
            <Alert severity="info">
              Un ejecutivo se pondrá en contacto con usted en las próximas 24 horas
              para continuar con el proceso de formalización del crédito.
            </Alert>
          )}
        </Box>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose} variant="contained" color="primary" size="large">
          Cerrar
        </Button>
      </DialogActions>
    </Dialog>
  );
}

