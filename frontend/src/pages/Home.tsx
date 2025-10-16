/**
 * Página de inicio con formulario de solicitud
 */
import { Box, Container } from '@mui/material';
import CreditApplicationForm from '../components/CreditApplicationForm';

export default function Home() {
  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <CreditApplicationForm />
      </Box>
    </Container>
  );
}

