"use client";

import type { FeatureImportanceItem } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

interface FeatureChartProps {
  features: FeatureImportanceItem[];
}

function cleanFeatureName(raw: string): string {
  // Convert snake_case feature names to readable labels
  return raw
    .replace(/^(brand_|payment_method_|product_category_|sub_category_|fulfillment_type_)/, (m) =>
      m.replace(/_$/, ": ").replace(/_/g, " "),
    )
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export function FeatureChart({ features }: FeatureChartProps) {
  if (features.length === 0) {
    return (
      <Card className="border-border/50 bg-card/60 backdrop-blur-sm">
        <CardContent className="flex items-center justify-center py-8">
          <p className="text-sm text-muted-foreground">
            Loading feature importance…
          </p>
        </CardContent>
      </Card>
    );
  }

  const top15 = features.slice(0, 15);
  const maxVal = top15[0]?.importance ?? 1;

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
              d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 0 0-2.455 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z"
            />
          </svg>
          Top Feature Importance
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-2">
        {top15.map((f, i) => {
          const pct = (f.importance / maxVal) * 100;
          const label = cleanFeatureName(f.feature);

          return (
            <Tooltip key={f.feature}>
              <TooltipTrigger>
                <div className="group flex items-center gap-3 cursor-default w-full">
                  <span className="text-xs text-muted-foreground w-[140px] truncate text-right shrink-0">
                    {label}
                  </span>
                  <div className="flex-1 h-2 rounded-full bg-muted/60 overflow-hidden">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-primary to-chart-5 bar-animate group-hover:brightness-125 transition-all"
                      style={{
                        width: `${pct}%`,
                        animationDelay: `${i * 60}ms`,
                      }}
                    />
                  </div>
                  <span className="text-xs font-mono text-muted-foreground w-12 text-right">
                    {f.importance.toFixed(2)}
                  </span>
                </div>
              </TooltipTrigger>
              <TooltipContent side="top">
                <p className="text-xs">
                  {f.feature}: {f.importance.toFixed(4)}
                </p>
              </TooltipContent>
            </Tooltip>
          );
        })}
      </CardContent>
    </Card>
  );
}
