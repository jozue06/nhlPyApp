import { API_BASE_URL } from "./apiConfig";
import {
  useState,
  useCallback,
  FormEvent,
  ChangeEvent,
  KeyboardEvent,
} from "react";
import ResultList from "./ResultList";

type FormState = {
  value: string;
  data: any[] | null;
  loading: boolean;
};

export const Form = () => {
  const [state, setState] = useState<FormState>({
    value: "",
    data: null,
    loading: false,
  });

  const handleChange = useCallback(
    (event: ChangeEvent<HTMLTextAreaElement>) => {
      setState((prev) => ({ ...prev, value: event.target.value }));
    },
    []
  );

  const handleSubmit = useCallback(
    async (event: FormEvent<HTMLFormElement>) => {
      setState((prev) => ({ ...prev, loading: true }));
      event.preventDefault();

      try {
        const response = await fetch(`${API_BASE_URL}/api/json/search`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            queryString: state.value,
          }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        setState((prev) => ({
          ...prev,
          data,
          loading: false,
        }));
      } catch {
        setState((prev) => ({ ...prev, loading: false }));
      }
    },
    [state.value]
  );

  const onKeyPress = useCallback(
    (event: KeyboardEvent<HTMLTextAreaElement>) => {
      if (event.which === 13) {
        // Create a synthetic form event
        const formEvent = {
          preventDefault: () => event.preventDefault(),
          currentTarget: event.currentTarget.form,
        } as FormEvent<HTMLFormElement>;

        handleSubmit(formEvent);
        event.preventDefault();
      }
    },
    [handleSubmit]
  );

  return (
    <div className="input-wrapper">
      <h6>This is the React.js version of the NHL Prospect Terminal App</h6>
      <form onSubmit={handleSubmit}>
        <textarea
          id="textareainput"
          value={state.value}
          onChange={handleChange}
          onKeyUp={onKeyPress}
          name="queryString"
          className="terminal"
          autoFocus={true}
          rows={10}
          cols={100}
        />
        <button type="submit" disabled={state.loading}>
          {state.loading ? "Loading..." : "Submit"}
        </button>
      </form>

      <div style={{ color: "aqua" }}>
        {state.data && <ResultList results={state.data} />}
      </div>
    </div>
  );
};
