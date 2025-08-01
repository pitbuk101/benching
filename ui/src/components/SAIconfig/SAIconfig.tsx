import { useState, useEffect } from 'react';
import styled from 'styled-components';
import {
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Switch,
  Button,
  Paper,
  CircularProgress,
} from '@mui/material';

const PageContainer = styled.div`
  max-width: 700px;
  margin: 40px auto;
  padding: 30px;
  background-color: #fafafa;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 24px;
`;

const Section = styled(Paper)`
  padding: 20px;
  border-radius: 10px;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  gap: 16px;
`;

const FlexRow = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const SaiConfig = () => {
  const [tenantIds, setTenantIds] = useState<string[]>([]);
  const [selectedTenant, setSelectedTenant] = useState('');
  const [adaServices, setAdaServices] = useState({
    charts: true,
    text_to_speech: true,
    speech_to_text: true,
    recommendation: true,
  });
  const [loadingTenants, setLoadingTenants] = useState(false);
  const [loadingServices, setLoadingServices] = useState(false);
  const [error, setError] = useState('');
  const [submitted, setSubmitted] = useState(false);

  // Fetch tenant IDs on mount
  useEffect(() => {
    setLoadingTenants(true);
    fetch(`${process.env.SAI_CONFIG_END_POINT}/all-tenants`) // replace with your actual API endpoint
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch tenant IDs');
        return res.json();
      })
      .then((data) => {
        setTenantIds(data.tenant_ids || []);
        setLoadingTenants(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoadingTenants(false);
      });
  }, []);

  // Fetch service toggles when tenant changes
  useEffect(() => {
    if (!selectedTenant) return;
    setLoadingServices(true);
    fetch(`${process.env.SAI_CONFIG_END_POINT}/tenant_config/${selectedTenant}`) // replace with your actual API endpoint
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch tenant config');
        return res.json();
      })
      .then((data) => {
        setAdaServices(
          data.ada || {
            charts: true,
            text_to_speech: true,
            speech_to_text: true,
            recommendation: true,
          },
        );
        setLoadingServices(false);
        setSubmitted(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoadingServices(false);
      });
  }, [selectedTenant]);

  const handleToggle = (service: keyof typeof adaServices) => {
    setAdaServices((prev) => ({
      ...prev,
      [service]: !prev[service],
    }));
  };

  const handleSubmit = () => {
    if (!selectedTenant) {
      setError('Please select a tenant');
      return;
    }

    setError('');
    const payload = {
      tenant_id: selectedTenant,
      ada: adaServices,
    };

    fetch(`${process.env.SAI_CONFIG_END_POINT}/ada-config`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
      .then((res) => {
        if (!res.ok) throw new Error('Failed to update tenant config');
        return res.json();
      })
      .then(() => {
        setSubmitted(true);
      })
      .catch((err) => {
        setError(err.message);
      });
  };

  const handleReset = () => {
    setSelectedTenant('');
    setAdaServices({
      charts: true,
      text_to_speech: true,
      speech_to_text: true,
      recommendation: true,
    });
    setError('');
    setSubmitted(false);
  };

  return (
    <PageContainer>
      <Typography variant="h4" component="h1">
        Source AI Config
      </Typography>

      {error && <Typography color="error">{error}</Typography>}

      <FormControl
        fullWidth
        variant="outlined"
        disabled={submitted || loadingTenants}
      >
        <InputLabel id="tenant-select-label">
          Select Tenant ID<span style={{ color: 'red' }}> *</span>
        </InputLabel>
        <Select
          labelId="tenant-select-label"
          value={selectedTenant}
          onChange={(e) => setSelectedTenant(e.target.value)}
          label="Select Tenant ID"
        >
          {loadingTenants ? (
            <MenuItem value="">
              <em>Loading...</em>
            </MenuItem>
          ) : (
            tenantIds.map((id) => (
              <MenuItem key={id} value={id}>
                {id}
              </MenuItem>
            ))
          )}
        </Select>
      </FormControl>

      <Section>
        <Typography variant="h6" component="h2" gutterBottom>
          ADA Services
        </Typography>
        {loadingServices ? (
          <CircularProgress />
        ) : (
          Object.entries(adaServices).map(([key, value]) => (
            <FlexRow key={key}>
              <Typography variant="body1">
                {key
                  .replace(/_/g, ' ')
                  .replace(/\b\w/g, (c) => c.toUpperCase())}
              </Typography>
              <Switch
                checked={value}
                onChange={() => handleToggle(key as keyof typeof adaServices)}
                disabled={submitted}
              />
            </FlexRow>
          ))
        )}
      </Section>

      <Button
        variant="contained"
        color="primary"
        onClick={submitted ? handleReset : handleSubmit}
        disabled={loadingTenants || loadingServices}
      >
        {submitted ? 'Reset' : 'Submit Config'}
      </Button>
    </PageContainer>
  );
};

export default SaiConfig;
