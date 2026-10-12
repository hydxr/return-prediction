import { Badge } from "@/components/ui/badge";

export function Header() {
  return (
    <header className="border-b border-border/50 backdrop-blur-sm bg-background/60 sticky top-0 z-50">
      <div className="max-w-[1440px] mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          {/* Icon */}
          <div className="size-9 rounded-lg bg-gradient-to-br from-primary to-chart-5 flex items-center justify-center">
            <svg
              className="size-5 text-primary-foreground"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285Z"
              />
            </svg>
          </div>

          <div>
            <h1 className="text-lg font-semibold tracking-tight">
              Return Predictor
            </h1>
            <p className="text-xs text-muted-foreground">
              E-Commerce Intelligence
            </p>
          </div>
        </div>

        <Badge variant="secondary" className="text-xs font-mono">
          ML Powered
        </Badge>
      </div>
    </header>
  );
}
