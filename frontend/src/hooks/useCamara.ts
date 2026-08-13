import { useState } from 'react';

export interface CamaraEstado {
  fotoUri: string | null;
  capturando: boolean;
  tomarFoto: (uri: string) => void;
  limpiarFoto: () => void;
}

export function useCamara(): CamaraEstado {
  const [fotoUri, setFotoUri] = useState<string | null>(null);
  const [capturando, setCapturando] = useState<boolean>(false);

  const tomarFoto = (uri: string) => {
    setFotoUri(uri);
    setCapturando(false);
  };

  const limpiarFoto = () => {
    setFotoUri(null);
  };

  return { fotoUri, capturando, tomarFoto, limpiarFoto };
}
