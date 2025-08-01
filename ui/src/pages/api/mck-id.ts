import { Mid } from '@mid/sdk';

let mid: Mid;
export function buildMid(): Mid {
  if (typeof window !== 'undefined') {
    mid = new Mid({
      loginInfo: {
        appId: `${process.env.NEXT_PUBLIC_OIDC_CLIENT_ID}`,
        authDriver: 'mid',
        flow: 'auth_code',
        oidcConfigUrl: `${process.env.NEXT_PUBLIC_OIDC_CONFIG_URL}`,
        fm: `${process.env.NEXT_PUBLIC_OIDC_FM}`,
      },
      logoutRedirectUrl: `${process.env.NEXT_PUBLIC_REDIRECT_BASE_URL}`,
      redirectUrl: `${process.env.NEXT_PUBLIC_REDIRECT_BASE_URL}/login/callback`,
    });
  }
  return mid;
}
