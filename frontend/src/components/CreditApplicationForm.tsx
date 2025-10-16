/**
 * Formulario de solicitud de crédito
 */
import { useState, useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  Grid,
  FormControlLabel,
  Checkbox,
  MenuItem,
  CircularProgress,
  Alert,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { crearSolicitud, getSucursales } from '../api';
import type { Sucursal, SolicitudResponse } from '../types';
import ResultModal from './ResultModal';

// Esquema de validación con Zod
const solicitudSchema = z.object({
  nombre: z.string().min(1, 'El nombre es requerido'),
  apellido: z.string().min(1, 'El apellido es requerido'),
  email: z.string().email('Email inválido'),
  telefono: z.string().optional(),
  fecha_nacimiento: z.string().min(1, 'La fecha de nacimiento es requerida'),
  // edad se calcula automáticamente en el backend
  monto_solicitado: z.number().min(1000, 'El monto mínimo es $1,000'),
  ingreso_mensual: z.number().min(1, 'El ingreso mensual es requerido'),
  score_crediticio: z
    .number()
    .min(300, 'Score mínimo 300')
    .max(850, 'Score máximo 850'),
  tiene_tarjeta_credito: z.boolean(),
  tiene_credito_automotriz: z.boolean(),
  plazo_meses: z.number().min(1, 'El plazo es requerido'),
  sucursal_id: z.number().min(1, 'Debe seleccionar una sucursal'),
});

type SolicitudFormData = z.infer<typeof solicitudSchema>;

export default function CreditApplicationForm() {
  const [sucursales, setSucursales] = useState<Sucursal[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [resultado, setResultado] = useState<SolicitudResponse | null>(null);
  const [modalOpen, setModalOpen] = useState(false);

  const {
    control,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<SolicitudFormData>({
    resolver: zodResolver(solicitudSchema),
    defaultValues: {
      nombre: '',
      apellido: '',
      email: '',
      telefono: '',
      fecha_nacimiento: '',
      // edad se calcula automáticamente
      monto_solicitado: 0,
      ingreso_mensual: 0,
      score_crediticio: 650,
      tiene_tarjeta_credito: false,
      tiene_credito_automotriz: false,
      plazo_meses: 12,
      sucursal_id: 0,
    },
  });

  // La edad se calcula automáticamente en el backend

  // Cargar sucursales
  useEffect(() => {
    const cargarSucursales = async () => {
      try {
        const data = await getSucursales();
        setSucursales(data);
      } catch (err) {
        console.error('Error cargando sucursales:', err);
        setError('Error al cargar sucursales');
      }
    };
    cargarSucursales();
  }, []);

  const onSubmit = async (data: SolicitudFormData) => {
    setLoading(true);
    setError(null);

    try {
      const response = await crearSolicitud(data);
      setResultado(response);
      setModalOpen(true);
      reset();
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Error al procesar la solicitud';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleCloseModal = () => {
    setModalOpen(false);
    setResultado(null);
  };

  return (
    <>
      <Paper elevation={3} sx={{ p: 4, maxWidth: 900, mx: 'auto', mt: 4 }}>
        <Typography variant="h4" gutterBottom align="center">
          Solicitud de Crédito
        </Typography>
        <Typography variant="body2" color="text.secondary" align="center" sx={{ mb: 3 }}>
          Complete el formulario para solicitar su crédito
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        <Box component="form" onSubmit={handleSubmit(onSubmit)}>
          <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
            Datos Personales
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <Controller
                name="nombre"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Nombre"
                    fullWidth
                    error={!!errors.nombre}
                    helperText={errors.nombre?.message}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Controller
                name="apellido"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Apellido"
                    fullWidth
                    error={!!errors.apellido}
                    helperText={errors.apellido?.message}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Controller
                name="email"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Email"
                    type="email"
                    fullWidth
                    error={!!errors.email}
                    helperText={errors.email?.message}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Controller
                name="telefono"
                control={control}
                render={({ field }) => (
                  <TextField {...field} label="Teléfono (opcional)" fullWidth />
                )}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Controller
                name="fecha_nacimiento"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Fecha de Nacimiento"
                    type="date"
                    fullWidth
                    InputLabelProps={{ shrink: true }}
                    error={!!errors.fecha_nacimiento}
                    helperText={errors.fecha_nacimiento?.message}
                  />
                )}
              />
            </Grid>
          </Grid>

          <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
            Información Financiera
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <Controller
                name="ingreso_mensual"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Ingreso Mensual"
                    type="number"
                    fullWidth
                    onChange={(e) => field.onChange(parseFloat(e.target.value) || 0)}
                    error={!!errors.ingreso_mensual}
                    helperText={errors.ingreso_mensual?.message}
                    InputProps={{ startAdornment: '$' }}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Controller
                name="score_crediticio"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Score Crediticio (300-850)"
                    type="number"
                    fullWidth
                    onChange={(e) => field.onChange(parseInt(e.target.value) || 0)}
                    error={!!errors.score_crediticio}
                    helperText={errors.score_crediticio?.message}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Controller
                name="tiene_tarjeta_credito"
                control={control}
                render={({ field }) => (
                  <FormControlLabel
                    control={<Checkbox {...field} checked={field.value} />}
                    label="Tengo tarjeta de crédito"
                  />
                )}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Controller
                name="tiene_credito_automotriz"
                control={control}
                render={({ field }) => (
                  <FormControlLabel
                    control={<Checkbox {...field} checked={field.value} />}
                    label="Tengo crédito automotriz"
                  />
                )}
              />
            </Grid>
          </Grid>

          <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
            Detalles del Crédito
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <Controller
                name="monto_solicitado"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Monto Solicitado"
                    type="number"
                    fullWidth
                    onChange={(e) => field.onChange(parseFloat(e.target.value) || 0)}
                    error={!!errors.monto_solicitado}
                    helperText={errors.monto_solicitado?.message}
                    InputProps={{ startAdornment: '$' }}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Controller
                name="plazo_meses"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Plazo (meses)"
                    select
                    fullWidth
                    onChange={(e) => field.onChange(parseInt(e.target.value))}
                    error={!!errors.plazo_meses}
                    helperText={errors.plazo_meses?.message}
                  >
                    <MenuItem value={12}>12 meses</MenuItem>
                    <MenuItem value={24}>24 meses</MenuItem>
                    <MenuItem value={36}>36 meses</MenuItem>
                    <MenuItem value={48}>48 meses</MenuItem>
                    <MenuItem value={60}>60 meses</MenuItem>
                  </TextField>
                )}
              />
            </Grid>
            <Grid item xs={12}>
              <Controller
                name="sucursal_id"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Sucursal"
                    select
                    fullWidth
                    onChange={(e) => field.onChange(parseInt(e.target.value))}
                    error={!!errors.sucursal_id}
                    helperText={errors.sucursal_id?.message}
                  >
                    <MenuItem value={0}>Seleccione una sucursal</MenuItem>
                    {sucursales.map((sucursal) => (
                      <MenuItem key={sucursal.id} value={sucursal.id}>
                        {sucursal.nombre} - {sucursal.ciudad}
                      </MenuItem>
                    ))}
                  </TextField>
                )}
              />
            </Grid>
          </Grid>

          <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
            <Button
              type="submit"
              variant="contained"
              size="large"
              disabled={loading}
              startIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
            >
              {loading ? 'Procesando...' : 'Enviar Solicitud'}
            </Button>
          </Box>
        </Box>
      </Paper>

      <ResultModal open={modalOpen} onClose={handleCloseModal} resultado={resultado} />
    </>
  );
}

