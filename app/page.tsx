import DoodleCanvas from "@/components/doodle-canvas"

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <div className="container mx-auto px-4 py-10">
        <h1 className="text-4xl font-bold text-center mb-2 text-slate-800 dark:text-slate-100">Doodle Recognition</h1>
        <p className="text-center mb-8 text-slate-600 dark:text-slate-300">
          Draw anything on the canvas and we&apos;ll recognize it 
        </p>
        <DoodleCanvas />
      </div>
    </main>
  )
}
