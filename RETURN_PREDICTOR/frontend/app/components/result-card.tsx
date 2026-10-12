"use client";

import type { PredictionResponse } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface ResultCardProps {
  result: PredictionResponse | null;
  loading: boolean;
}

const riskConfig = {
  Low: {
    color: "text-emerald-500",
    stroke: "stroke-emerald-500",
    bg: "bg-emerald-500/10",
    badgeClass: "bg-emerald-500/15 text-emerald-500 border-emerald-500/30",
    label: "Low Risk",
  },
  Medium: {
    color: "text-amber-500",
    stroke: "stroke-amber-500",
    bg: "bg-amber-500/10",
    badgeClass: "bg-amber-500/15 text-amber-500 border-amber-500/30",
    label: "Medium Risk",
  },
  High: {
    color: "text-rose-500",
    stroke: "stroke-rose-500",
    bg: "bg-rose-500/10",
    badgeClass: "bg-rose-500/15 text-rose-500 border-rose-500/30",
    label: "High Risk",
  },
} as const;

function RiskGauge({
  probability,
  risk,
}: {
  probability: number;
  risk: "Low" | "Medium" | "High";
}) {
  const cfg = riskConfig[risk];
  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  // Semi-circle: use half circumference
  const half = circumference / 2;
  const filled = half * probability;

  return (
    <div className="flex flex-col items-center gap-2">
      <svg
        width="160"
        height="90"
        viewBox="0 0 160 90"
        className="drop-shadow-lg"
      >
        {/* Background arc */}
        <path
          d="M 10 80 A 40 40 0 0 1 150 80"
          fill="none"
          strokeWidth="12"
          strokeLinecap="round"
          className="stroke-muted"
        />
        {/* Filled arc */}
        <path
          d="M 10 80 A 40 40 0 0 1 150 80"
          fill="none"
          strokeWidth="12"
          strokeLinecap="round"
          className={`${cfg.stroke} gauge-animate`}
          strokeDasharray={`${filled} ${half}`}
        />
        {/* Probability text */}
        <text
          x="80"
          y="70"
          textAnchor="middle"
          className={`${cfg.color} text-2xl font-bold`}
          fill="currentColor"
        >
          {(probability * 100).toFixed(1)}%
        </text>
      </svg>

      <Badge variant="outline" className={cfg.badgeClass}>
        <span className={`inline-block size-2 rounded-full ${cfg.bg} ${cfg.color} pulse-glow mr-1.5`}>
          <span className={`block size-2 rounded-full ${risk === "Low" ? "bg-emerald-500" : risk === "Medium" ? "bg-amber-500" : "bg-rose-500"}`} />
        </span>
        {cfg.label}
      </Badge>
    </div>
  );
}

export function ResultCard({ result, loading }: ResultCardProps) {
  if (loading) {
    return (
      <Card className="border-border/50 bg-card/60 backdrop-blur-sm">
        <CardContent className="flex items-center justify-center py-12">
          <div className="flex flex-col items-center gap-3">
            <div className="size-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
            <p className="text-sm text-muted-foreground">
              Analyzing order…
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!result) {
    return (
      <Card className="border-border/50 bg-card/60 backdrop-blur-sm border-dashed">
        <CardContent className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="size-12 mx-auto mb-3 rounded-full bg-muted flex items-center justify-center">
              <svg
                className="size-6 text-muted-foreground"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z"
                />
              </svg>
            </div>
            <p className="text-sm text-muted-foreground">
              Fill in order details and click <strong>Predict</strong>
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="border-border/50 bg-card/60 backdrop-blur-sm fade-up">
      <CardHeader className="pb-2">
        <CardTitle className="text-base">Prediction Result</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col items-center gap-4 pt-2">
        <RiskGauge
          probability={result.return_probability}
          risk={result.risk_level}
        />

        <div className="w-full grid grid-cols-2 gap-3 text-sm">
          <div className="rounded-lg bg-muted/50 p-3 text-center">
            <p className="text-muted-foreground text-xs mb-1">Probability</p>
            <p className="font-semibold font-mono">
              {(result.return_probability * 100).toFixed(2)}%
            </p>
          </div>
          <div className="rounded-lg bg-muted/50 p-3 text-center">
            <p className="text-muted-foreground text-xs mb-1">Prediction</p>
            <p className="font-semibold">
              {result.predicted_returned ? "Will Return" : "Won't Return"}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
