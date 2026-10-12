"use client";

import { useState } from "react";
import type { OrderInput, PredictionResponse } from "@/lib/api";
import { predictReturn } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";

interface PredictionFormProps {
  onResult: (result: PredictionResponse) => void;
  onLoading: (loading: boolean) => void;
}

const DEFAULTS: OrderInput = {
  product_category: "Electronics",
  sub_category: "Smartphones",
  brand: "Brand_1",
  product_price: 500,
  discount_percent: 15,
  product_rating: 4.2,
  review_count: 120,
  fragile_item: 0,
  warranty_available: 1,
  product_return_rate: 0.12,
  category_return_rate: 0.18,
  brand_return_rate: 0.1,
  defect_rate: 0.03,
  seller_rating: 4.5,
  seller_return_rate: 0.08,
  fulfillment_type: "Marketplace Fulfilled",
  payment_method: "Credit Card",
  quantity: 1,
  shipping_distance_km: 250,
  delayed_delivery: 0,
  wishlist_before_purchase: 1,
  product_page_views: 35,
  customer_support_calls: 1,
  chat_interactions: 0,
};

type FieldConfig = {
  key: keyof OrderInput;
  label: string;
  type: "number" | "select" | "toggle";
  options?: string[];
  step?: string;
  min?: number;
  max?: number;
};

const FIELD_GROUPS: { title: string; icon: string; fields: FieldConfig[] }[] = [
  {
    title: "Product",
    icon: "🛍️",
    fields: [
      {
        key: "product_category",
        label: "Category",
        type: "select",
        options: ["Electronics", "Fashion", "Home & Kitchen", "Beauty", "Sports", "Books"],
      },
      {
        key: "sub_category",
        label: "Sub-category",
        type: "select",
        options: ["Smartphones", "Laptops", "Accessories", "Clothing", "Shoes", "Appliances"],
      },
      {
        key: "brand",
        label: "Brand",
        type: "select",
        options: Array.from({ length: 20 }, (_, i) => `Brand_${i + 1}`),
      },
      { key: "product_price", label: "Price (₹)", type: "number", step: "0.01", min: 0 },
      { key: "discount_percent", label: "Discount %", type: "number", step: "0.1", min: 0, max: 100 },
      { key: "product_rating", label: "Rating", type: "number", step: "0.1", min: 0, max: 5 },
      { key: "review_count", label: "Review Count", type: "number", min: 0 },
      { key: "quantity", label: "Quantity", type: "number", min: 1 },
      { key: "fragile_item", label: "Fragile", type: "toggle" },
      { key: "warranty_available", label: "Warranty", type: "toggle" },
    ],
  },
  {
    title: "Risk Rates",
    icon: "📊",
    fields: [
      { key: "product_return_rate", label: "Product Return Rate", type: "number", step: "0.01", min: 0, max: 1 },
      { key: "category_return_rate", label: "Category Return Rate", type: "number", step: "0.01", min: 0, max: 1 },
      { key: "brand_return_rate", label: "Brand Return Rate", type: "number", step: "0.01", min: 0, max: 1 },
      { key: "defect_rate", label: "Defect Rate", type: "number", step: "0.01", min: 0, max: 1 },
    ],
  },
  {
    title: "Seller & Logistics",
    icon: "🚚",
    fields: [
      { key: "seller_rating", label: "Seller Rating", type: "number", step: "0.1", min: 0, max: 5 },
      { key: "seller_return_rate", label: "Seller Return Rate", type: "number", step: "0.01", min: 0, max: 1 },
      {
        key: "fulfillment_type",
        label: "Fulfillment",
        type: "select",
        options: ["Marketplace Fulfilled", "Seller Fulfilled"],
      },
      { key: "shipping_distance_km", label: "Distance (km)", type: "number", step: "0.1", min: 0 },
      { key: "delayed_delivery", label: "Delayed", type: "toggle" },
    ],
  },
  {
    title: "Customer",
    icon: "👤",
    fields: [
      {
        key: "payment_method",
        label: "Payment",
        type: "select",
        options: ["Credit Card", "Debit Card", "UPI", "COD", "Net Banking", "EMI"],
      },
      { key: "wishlist_before_purchase", label: "Wishlisted", type: "toggle" },
      { key: "product_page_views", label: "Page Views", type: "number", min: 0 },
      { key: "customer_support_calls", label: "Support Calls", type: "number", min: 0 },
      { key: "chat_interactions", label: "Chat Messages", type: "number", min: 0 },
    ],
  },
];

export function PredictionForm({ onResult, onLoading }: PredictionFormProps) {
  const [form, setForm] = useState<OrderInput>(DEFAULTS);
  const [error, setError] = useState<string | null>(null);

  function updateField(key: keyof OrderInput, value: string | number) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    onLoading(true);

    try {
      const result = await predictReturn(form);
      onResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Prediction failed");
    } finally {
      onLoading(false);
    }
  }

  function handleReset() {
    setForm(DEFAULTS);
    setError(null);
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
              d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
            />
          </svg>
          Order Details
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-5">
          {FIELD_GROUPS.map((group, gi) => (
            <div key={group.title}>
              {gi > 0 && <Separator className="mb-4" />}
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-3">
                {group.icon} {group.title}
              </p>
              <div className="grid grid-cols-2 gap-x-4 gap-y-3">
                {group.fields.map((field) => (
                  <div
                    key={field.key}
                    className={
                      field.type === "toggle" ? "flex items-center gap-2" : "space-y-1.5"
                    }
                  >
                    <Label
                      htmlFor={`field-${field.key}`}
                      className="text-xs text-muted-foreground"
                    >
                      {field.label}
                    </Label>

                    {field.type === "number" && (
                      <Input
                        id={`field-${field.key}`}
                        type="number"
                        step={field.step ?? "1"}
                        min={field.min}
                        max={field.max}
                        value={form[field.key] as number}
                        onChange={(e) =>
                          updateField(field.key, parseFloat(e.target.value) || 0)
                        }
                        className="h-8 text-sm bg-background/50"
                      />
                    )}

                    {field.type === "select" && (
                      <Select
                        value={form[field.key] as string}
                        onValueChange={(v) => { if (v != null) updateField(field.key, v); }}
                      >
                        <SelectTrigger
                          id={`field-${field.key}`}
                          className="h-8 text-sm bg-background/50"
                        >
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {field.options?.map((opt) => (
                            <SelectItem key={opt} value={opt}>
                              {opt}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    )}

                    {field.type === "toggle" && (
                      <button
                        type="button"
                        role="switch"
                        aria-checked={(form[field.key] as number) === 1}
                        onClick={() =>
                          updateField(
                            field.key,
                            (form[field.key] as number) === 1 ? 0 : 1,
                          )
                        }
                        className={`relative inline-flex h-5 w-9 items-center rounded-full transition-colors ${
                          (form[field.key] as number) === 1
                            ? "bg-primary"
                            : "bg-muted"
                        }`}
                      >
                        <span
                          className={`inline-block size-3.5 rounded-full bg-white shadow-sm transition-transform ${
                            (form[field.key] as number) === 1
                              ? "translate-x-[18px]"
                              : "translate-x-[3px]"
                          }`}
                        />
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}

          {error && (
            <div className="rounded-lg bg-destructive/10 border border-destructive/30 p-3 text-sm text-destructive">
              {error}
            </div>
          )}

          <div className="flex gap-3 pt-1">
            <Button type="submit" className="flex-1 cursor-pointer">
              <svg
                className="size-4 mr-1.5"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z"
                />
              </svg>
              Predict
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={handleReset}
              className="cursor-pointer"
            >
              Reset
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
