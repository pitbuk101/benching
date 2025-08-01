'use client';
import styled from '@emotion/styled';
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import React from 'react';

const LoadingStyle = {
  alignItems: 'center',
  backgroundColor: '#F5F5F5;',
  display: 'flex',
  justifyContent: 'center',
  width: '100%',
  height: '100%',
};
const LoadingWrapper = styled.div`
  display: flex;
  width: 100vw;
  height: 100vh;
  text-align: center;
`;
const theme = createTheme({
  palette: {
    primary: {
      main: '#2151FE',
    },
  },
});

interface LoaderProps {
  size?: number;
  isLoading?: boolean;
  errorMsg?: string;
}

const AuthLoader = ({ size }: LoaderProps) => {
  return (
    <ThemeProvider theme={theme}>
      <LoadingWrapper data-testid="loading-wrapper">
        <Box sx={LoadingStyle}>
          <CircularProgress color="primary" size={size} thickness={4} />
        </Box>
      </LoadingWrapper>
    </ThemeProvider>
  );
};
export default AuthLoader;
