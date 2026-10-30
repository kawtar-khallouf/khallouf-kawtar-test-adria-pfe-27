import Keycloak from 'keycloak-js';
export const auth = new Keycloak({url:'http://localhost:8085',realm:'bank',clientId:'bank-ui'});
export async function initAuth(){
  try { await auth.init({onLoad:'check-sso',pkceMethod:'S256',checkLoginIframe:false}); }
  catch(e){ console.warn('Keycloak unavailable. Start Docker Compose or use unsecured local API.', e); }
}
export async function token(){
  if (!auth.authenticated) return '';
  await auth.updateToken(30);
  return auth.token || '';
}
