import { useEffect, useRef } from "react";

declare global {
  interface Window {
    google?: {
      accounts: {
        id: {
          initialize: (config: {
            client_id: string;
            callback: (response: { credential: string }) => void;
          }) => void;
          renderButton: (
            parent: HTMLElement,
            options: {
              theme?: string;
              size?: string;
              text?: string;
              shape?: string;
            },
          ) => void;
          prompt: () => void;
        };
      };
    };
  }
}

export type GoogleButtonOptions = {
  theme?: "outline" | "filled_blue" | "filled_black";
  size?: "large" | "medium" | "small";
  text?: "signin_with" | "signup_with" | "continue_with" | "signin";
  shape?: "rectangular" | "pill" | "circle" | "square";
};

export type UseGoogleLoginResult = {
  buttonRef: React.RefObject<HTMLDivElement | null>;
};

export const useGoogleLogin = (
  clientId: string,
  onCredentialReceived: (credential: string) => void,
  buttonOptions?: GoogleButtonOptions,
): UseGoogleLoginResult => {
  const buttonRef = useRef<HTMLDivElement | null>(null);
  const callbackRef = useRef(onCredentialReceived);
  const initializedRef = useRef(false);

  useEffect(() => {
    callbackRef.current = onCredentialReceived;
  }, [onCredentialReceived]);

  useEffect(() => {
    const handleGoogleCallback = (response: { credential: string }) => {
      callbackRef.current(response.credential);
    };

    const initializeGoogleButton = () => {
      if (window.google && buttonRef.current && !initializedRef.current) {
        initializedRef.current = true;

        window.google.accounts.id.initialize({
          client_id: clientId,
          callback: handleGoogleCallback,
        });

        window.google.accounts.id.renderButton(buttonRef.current, {
          theme: buttonOptions?.theme || "outline",
          size: buttonOptions?.size || "large",
          text: buttonOptions?.text || "signin_with",
          shape: buttonOptions?.shape || "rectangular",
        });
      }
    };

    // try to initialize immediately if script is already loaded
    if (window.google) {
      initializeGoogleButton();
    } else {
      // if script not loaded yet, wait for it
      const checkGoogleLoaded = setInterval(() => {
        if (window.google) {
          clearInterval(checkGoogleLoaded);
          initializeGoogleButton();
        }
      }, 100);

      // cleanup interval on unmount
      return () => clearInterval(checkGoogleLoaded);
    }
  }, [clientId, buttonOptions]);

  return {
    buttonRef,
  };
};
