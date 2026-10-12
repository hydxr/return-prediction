"use client";

import type { MetricItem } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface MetricsChartProps {
  metrics: MetricItem[];
}

const metricColors: Record<string, string> = {
  Accuracy: "bg-chart-1",
  Precision: "bg-chart-2",
  Recall: "bg-chart-3",
  F1: "bg-chart-5",
};

export function MetricsChart({ metrics }: MetricsChartProps) {
  if (metrics.length === 0) {
    return (
      <Card className="border-border/50 bg-card/60 backdrop-blur-sm">
        <CardContent className="flex items-center justify-center py-8">
          <p className="text-sm text-muted-foreground">Loading metrics…</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="border-border/50 bg-card/60 backdrop-blur-sm">
      <CardHeader className="pb-3">
        <CardTitle className="text-base flex items-center gap-2">
          <svg
            className="size-4 text-muted-foreground"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z"
            />
          </svg>
          Model Performance
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {metrics.map((m, i) => {
          const pct = m.value * 100;
          const color = metricColors[m.name] ?? "bg-primary";

          return (
            <div key={m.name} className="space-y-1.5">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">{m.name}</span>
                <span className="font-mono font-medium">
                  {pct.toFixed(1)}%
                </span>
              </div>
              <div className="h-2.5 rounded-full bg-muted/60 overflow-hidden">
                <div
                  className={`h-full rounded-full ${color} bar-animate`}
                  style={{
                    width: `${pct}%`,
                    animationDelay: `${i * 100}ms`,
                  }}
                />
              </div>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
}
