import { Routes, Route } from 'react-router-dom'

import Header from './components/Header.jsx'
import ExploreFooter from './components/ExploreFooter.jsx'
import Footer from './components/Footer.jsx'
import MapExplorer from './pages/MapExplorer.jsx'

import HomePage from './pages/Home.jsx'
import AboutPage from './pages/About.jsx'
import DataExplorer from './pages/DataExplorer.jsx'
import ElectricityAccess from './pages/ElectricityAccess.jsx'
import Infrastructure from './pages/Infrastructure.jsx'
import SolarPotential from './pages/SolarPotential.jsx'
import MiniGrid from './pages/MiniGrids.jsx'
import GeneratorUse from './pages/GeneratorUse.jsx'
import AssetOwnership from './pages/AssetOwnership.jsx'

function DefaultLayout({ children }) {
  return (
    <section className="flex flex-col min-h-screen">
      <Header />
      <div className="flex-grow">{children}</div>
      <Footer />
    </section>
  )
}

function ExploreLayout({ children }) {
  return (
    <section className="flex flex-col min-h-screen">
      <Header />
      <div className="flex-grow">{children}</div>
      <ExploreFooter />
    </section>
  )
}

function MapLayout({ children }) {
  return (
    <section className="flex flex-col min-h-screen">
      <Header />
      <div className="flex-grow flex flex-col overflow-hidden">
        {children}
      </div>
    </section>
  )
}

function App() {
  return (
    <main className="pt-20">
      <Routes>
        <Route path="/" element={
          <DefaultLayout>
            <HomePage />
          </DefaultLayout>
        } />
        
        <Route path="/about" element={
          <DefaultLayout>
            <AboutPage />
          </DefaultLayout>
        } />
        
        <Route path="/data" element={
          <MapLayout>
            <MapExplorer />
          </MapLayout>
        } />
        
        <Route path="/explore" element={
          <ExploreLayout>
            <DataExplorer />
          </ExploreLayout>
        } />
        
        <Route path="/explore/electricity" element={
          <ExploreLayout>
            <ElectricityAccess />
          </ExploreLayout>
        } />
        
        <Route path="/explore/infrastructure" element={
          <ExploreLayout>
            <Infrastructure />
          </ExploreLayout>
        } />
        
        <Route path="/explore/solar" element={
          <ExploreLayout>
            <SolarPotential />
          </ExploreLayout>
        } />
        
        <Route path="/explore/minigrids" element={
          <ExploreLayout>
            <MiniGrid />
          </ExploreLayout>
        } />
        
        <Route path="/explore/generator" element={
          <ExploreLayout>
            <GeneratorUse />
          </ExploreLayout>
        } />
        
        <Route path="/explore/assets" element={
          <ExploreLayout>
            <AssetOwnership />
          </ExploreLayout>
        } />
      </Routes>
    </main>
  )
}

export default App;