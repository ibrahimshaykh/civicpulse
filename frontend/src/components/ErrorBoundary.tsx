import { Component, type ErrorInfo, type ReactNode } from "react";

type Props = { children: ReactNode; fallback?: (err: Error, reset: () => void) => ReactNode };
type State = { error: Error | null };

export class ErrorBoundary extends Component<Props, State> {
  override state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  override componentDidCatch(error: Error, info: ErrorInfo) {
    console.error(JSON.stringify({ level: "error", msg: "ui_crash", error: error.message, stack: info.componentStack }));
  }

  reset = () => {
    this.setState({ error: null });
  };

  override render() {
    if (this.state.error) {
      return (
        this.props.fallback?.(this.state.error, this.reset) ?? (
          <div role="alert" className="p-6">
            <h2 className="text-lg font-semibold">This page stopped working</h2>
            <p className="mt-2">Reload the page. If it keeps happening, note the time and report it.</p>
            <button type="button" className="btn mt-4" onClick={this.reset}>
              Try again
            </button>
          </div>
        )
      );
    }
    return this.props.children;
  }
}
