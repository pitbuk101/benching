/* eslint-disable @typescript-eslint/no-var-requires */
const dotenv = require('dotenv');
const path = require('path');
const withLess = require('next-with-less');
const fs = require('fs');

const currentDirectory = __dirname;

console.log('New env to check look', { NODE_ENV: process.env.NODE_ENV });

const files = fs.readdirSync(currentDirectory);
console.log('Contents of the current directory:');
files.forEach((file) => {
  console.log(file);
});

dotenv.config({ path: `./.env.${process.env.NODE_ENV}` });

const resolveAlias = {
  antd$: path.resolve(__dirname, 'node_modules/antd/lib'),
  '@ant-design/icons$': path.resolve(
    __dirname,
    'node_modules/@ant-design/icons/lib',
  ),
};

/** @type {import('next').NextConfig} */
const nextConfig = withLess({
  output: 'standalone',
  staticPageGenerationTimeout: 1000,
  compiler: {
    // Enables the styled-components SWC transform
    styledComponents: {
      displayName: true,
      ssr: true,
    },
  },
  lessLoaderOptions: {
    additionalData: `@import "@/styles/antd-variables.less";`,
  },
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      ...resolveAlias,
    };
    return config;
  },
  // routes redirect
  async redirects() {
    return [
      {
        source: '/setup',
        destination: '/setup/connection',
        permanent: true,
      },
    ];
  },
  env: {
    NEXT_PUBLIC_OIDC_CLIENT_ID: process.env.NEXT_PUBLIC_OIDC_CLIENT_ID,
    NEXT_PUBLIC_REDIRECT_BASE_URL: process.env.NEXT_PUBLIC_REDIRECT_BASE_URL,
    NEXT_PUBLIC_OIDC_CONFIG_URL: process.env.NEXT_PUBLIC_OIDC_CONFIG_URL,
    NEXT_PUBLIC_OIDC_FM: process.env.NEXT_PUBLIC_OIDC_FM,
    ADMIN_END_POINT: process.env.NEXT_PUBLIC_ADMIN_END_POINT,
    CLIENT_ONBORDING_END_POINT: process.env.CLIENT_ONBORDING_END_POINT,
    ADMIN_MARKET_RADAR_END_POINT: process.env.ADMIN_MARKET_RADAR_END_POINT,
    SAI_CONFIG_END_POINT: process.env.SAI_CONFIG_END_POINT,
  },
});

module.exports = nextConfig;
