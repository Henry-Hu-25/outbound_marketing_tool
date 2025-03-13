import { Input } from "@/components/ui/input";
import { Label } from "@radix-ui/react-label";
import { forwardRef, ChangeEvent } from "react";

interface UrlInputProps {
  label: string;
  placeholder: string;
  value: string;
  onChange: (e: ChangeEvent<HTMLInputElement>) => void;
}

export const UrlInput = forwardRef<HTMLInputElement, UrlInputProps>(
  ({ label, placeholder, value, onChange }, ref) => {
    return (
      <div className="w-full max-w-md space-y-2">
        <Label
          htmlFor={label.replace(/\s+/g, "-").toLowerCase()}
          className="text-sm font-medium text-foreground"
        >
          {label}
        </Label>
        <Input
          id={label.replace(/\s+/g, "-").toLowerCase()}
          type="url"
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          ref={ref}
          className="w-full bg-background/80 backdrop-blur-sm border-border"
        />
      </div>
    );
  }
);

UrlInput.displayName = "UrlInput"; 