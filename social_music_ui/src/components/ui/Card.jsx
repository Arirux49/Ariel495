export default function Card({ className = "", children }) {
  return (
    <div
      className={[
        "rounded-2xl bg-zinc-950/60 border border-zinc-800 shadow-xl",
        "p-4 md:p-6",
        className,
      ].join(" ")}
    >
      {children}
    </div>
  );
}
