import { RouterProvider } from "react-router-dom";
import { ThemeProvider } from "@/components/ThemeProvider";
import { router } from "./router";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./api/QueryClient";
import { useEffect } from "react";
import { initializeApiKey } from "./api/AxiosClient";

import { PostHogProvider } from "posthog-js/react";

const postHogOptions = {
  api_host: "https://app.posthog.com",
};

function App() {
  useEffect(() => {
    // Initialize API key when app starts
    initializeApiKey().catch(console.error);
  }, []);

  return (
    <PostHogProvider
      apiKey="phc_bVT2ugnZhMHRWqMvSRHPdeTjaPxQqT3QSsI3r5FlQR5"
      options={postHogOptions}
    >
      <QueryClientProvider client={queryClient}>
        <ThemeProvider defaultTheme="dark">
          <RouterProvider router={router} />
        </ThemeProvider>
      </QueryClientProvider>
    </PostHogProvider>
  );
}

export default App;
