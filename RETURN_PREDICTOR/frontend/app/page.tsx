"use client";

import { useEffect, useState } from "react";
import type {
  PredictionResponse,
  MetricItem,
  FeatureImportanceItem,
} from "@/lib/api";
import { fetchModelInfo } from "@/lib/api";
import { Header } from "@/components/header";
import { PredictionForm } from "@/components/prediction-form";
import { ResultCard } from "@/components/result-card";
import { MetricsChart } from "@/components/metrics-chart";
import { FeatureChart } from "@/components/feature-chart";
import { Badge } from "@/components/ui/badge";

export default function Dashboard() {
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [metrics, setMetrics] = useState<MetricItem[]>([]);
  const [features, setFeatures] = useState<FeatureImportanceItem[]>([]);
  const [modelName, setModelName] = useState("");
  const [infoError, setInfoError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const info = await fetchModelInfo();
        setMetrics(info.metrics);
        setFeatures(info.feature_importance);
        setModelName(info.model_name);
      } catch (err) {
        setInfoError(
          err instanceof Error ? err.message : "Failed to load model info",
        );
      }
    }
    load();
  }, []);

  return (
    <div className="flex flex-col min-h-full">
      <Header />

      <main className="flex-1 max-w-[1440px] w-full mx-auto px-6 py-6">
        {/* Model badge */}
        <div className="flex items-center gap-2 mb-6">
          {modelName && (
            <Badge variant="outline" className="text-xs font-mono">
              Model: {modelName}
            </Badge>
          )}
          {infoError && (
            <Badge variant="destructive" className="text-xs">
              ⚠ {infoError}
            </Badge>
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
          {/* Left panel: Form + Result (60%) */}
          <div className="lg:col-span-3 space-y-6">
            <PredictionForm onResult={setResult} onLoading={setLoading} />
            <ResultCard result={result} loading={loading} />
          </div>

          {/* Right panel: Charts (40%) */}
          <div className="lg:col-span-2 space-y-6">
            <MetricsChart metrics={metrics} />
            <FeatureChart features={features} />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border/50 mt-auto">
        <div className="max-w-[1440px] mx-auto px-6 py-4 flex items-center justify-between text-xs text-muted-foreground">
          <p>Product Return Prediction — Capstone Project</p>
          <p className="font-mono">FastAPI + Next.js</p>
        </div>
      </footer>
    </div>
  );
}
