'use client'

import Image from 'next/image'

import StorageTree from './components/storage_tree'

export default function Home() {
  return (
    <main className="h-screen">
    <div className="flex w-full bg-cyan-400 p-5">ETL Rules UI</div>
    <div className="flex p-5">
      <div className="flex-initial w-64 items-stretch">
        <StorageTree />
      </div>
      <div className="flex-auto items-stretch">Payload</div>
    </div>
    </main>
  )
}
