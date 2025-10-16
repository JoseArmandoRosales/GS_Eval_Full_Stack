/**
 * Dashboard de administrador con indicadores
 */
import { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { getIndicadores } from '../api';
import type { IndicadoresGenerales } from '../types';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import AssessmentIcon from '@mui/icons-material/Assessment';

const COLORS = ['#4caf50', '#f44336'];

export default function Dashboard() {
  const [indicadores, setIndicadores] = useState<IndicadoresGenerales | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const cargarIndicadores = async () => {
      try {
        const data = await getIndicadores();
        setIndicadores(data);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Error al cargar indicadores');
      } finally {
        setLoading(false);
      }
    };

    cargarIndicadores();
  }, []);

  if (loading) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '80vh',
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  if (error || !indicadores) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error">{error || 'Error al cargar datos'}</Alert>
      </Box>
    );
  }

  // Datos para gráfico de pie
  const pieData = [
    { name: 'Aprobadas', value: indicadores.total_aprobadas },
    { name: 'Rechazadas', value: indicadores.total_rechazadas },
  ];

  // Datos para gráfico de barras por sucursal
  const barData = indicadores.por_sucursal.map((sucursal) => ({
    nombre: sucursal.sucursal_nombre,
    aprobadas: sucursal.aprobadas,
    rechazadas: sucursal.rechazadas,
  }));

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Dashboard de Indicadores
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom sx={{ mb: 3 }}>
        Resumen general de solicitudes de crédito
      </Typography>

      {/* Tarjetas de resumen */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%', minHeight: 140 }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <AssessmentIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">Total Solicitudes</Typography>
              </Box>
              <Typography variant="h3">{indicadores.total_solicitudes}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%', minHeight: 140, backgroundColor: '#e8f5e9' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <TrendingUpIcon color="success" sx={{ mr: 1 }} />
                <Typography variant="h6">Aprobadas</Typography>
              </Box>
              <Typography variant="h3" color="success.main">
                {indicadores.total_aprobadas}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {indicadores.tasa_aprobacion.toFixed(1)}% de tasa
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%', minHeight: 140, backgroundColor: '#ffebee' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <TrendingDownIcon color="error" sx={{ mr: 1 }} />
                <Typography variant="h6">Rechazadas</Typography>
              </Box>
              <Typography variant="h3" color="error.main">
                {indicadores.total_rechazadas}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {(100 - indicadores.tasa_aprobacion).toFixed(1)}% de tasa
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%', minHeight: 140, backgroundColor: '#e3f2fd' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <AttachMoneyIcon color="info" sx={{ mr: 1 }} />
                <Typography variant="h6">Monto Aprobado</Typography>
              </Box>
              <Typography variant="h5" color="info.main">
                ${indicadores.monto_total_aprobado.toLocaleString('es-MX')}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Score Promedio: {indicadores.score_promedio.toFixed(0)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Gráficos */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Distribución de Solicitudes
            </Typography>
            <ResponsiveContainer width="100%" height={350}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) =>
                    `${name}: ${(percent * 100).toFixed(0)}%`
                  }
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Solicitudes por Sucursal
            </Typography>
            <ResponsiveContainer width="100%" height={350}>
              <BarChart data={barData} margin={{ top: 5, right: 30, left: 20, bottom: 80 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="nombre" 
                  angle={-35} 
                  textAnchor="end" 
                  height={90}
                  interval={0}
                  tick={{ fontSize: 12 }}
                />
                <YAxis />
                <Tooltip />
                <Legend wrapperStyle={{ paddingTop: '10px' }} />
                <Bar dataKey="aprobadas" fill="#4caf50" name="Aprobadas" />
                <Bar dataKey="rechazadas" fill="#f44336" name="Rechazadas" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      {/* Tabla de sucursales */}
      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Detalle por Sucursal
        </Typography>
        <Box sx={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ backgroundColor: '#f5f5f5' }}>
                <th style={{ padding: '12px', textAlign: 'left', borderBottom: '2px solid #ddd' }}>
                  Sucursal
                </th>
                <th style={{ padding: '12px', textAlign: 'left', borderBottom: '2px solid #ddd' }}>
                  Ciudad
                </th>
                <th style={{ padding: '12px', textAlign: 'center', borderBottom: '2px solid #ddd' }}>
                  Total
                </th>
                <th style={{ padding: '12px', textAlign: 'center', borderBottom: '2px solid #ddd' }}>
                  Aprobadas
                </th>
                <th style={{ padding: '12px', textAlign: 'center', borderBottom: '2px solid #ddd' }}>
                  Rechazadas
                </th>
                <th style={{ padding: '12px', textAlign: 'right', borderBottom: '2px solid #ddd' }}>
                  Monto Promedio
                </th>
                <th style={{ padding: '12px', textAlign: 'right', borderBottom: '2px solid #ddd' }}>
                  Total Aprobado
                </th>
              </tr>
            </thead>
            <tbody>
              {indicadores.por_sucursal.map((sucursal) => (
                <tr key={sucursal.sucursal_id}>
                  <td style={{ padding: '12px', borderBottom: '1px solid #ddd' }}>
                    {sucursal.sucursal_nombre}
                  </td>
                  <td style={{ padding: '12px', borderBottom: '1px solid #ddd' }}>
                    {sucursal.ciudad}
                  </td>
                  <td style={{ padding: '12px', textAlign: 'center', borderBottom: '1px solid #ddd' }}>
                    {sucursal.total_solicitudes}
                  </td>
                  <td style={{ padding: '12px', textAlign: 'center', borderBottom: '1px solid #ddd', color: '#4caf50' }}>
                    {sucursal.aprobadas}
                  </td>
                  <td style={{ padding: '12px', textAlign: 'center', borderBottom: '1px solid #ddd', color: '#f44336' }}>
                    {sucursal.rechazadas}
                  </td>
                  <td style={{ padding: '12px', textAlign: 'right', borderBottom: '1px solid #ddd' }}>
                    ${sucursal.monto_promedio.toLocaleString('es-MX', {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    })}
                  </td>
                  <td style={{ padding: '12px', textAlign: 'right', borderBottom: '1px solid #ddd' }}>
                    ${sucursal.monto_aprobado_total.toLocaleString('es-MX', {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    })}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Box>
      </Paper>
    </Box>
  );
}

