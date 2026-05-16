import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { 
  Activity, 
  ShoppingCart, 
  MapPin, 
  ShieldCheck, 
  MessageSquare, 
  TrendingUp,
  Clock,
  AlertTriangle
} from 'lucide-react';

// Leaflet icon fix for React
import L from 'leaflet';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: markerIcon,
    shadowUrl: markerShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

const HUBS = [
  { name: 'Santa', coords: [5.829, 10.158], status: 'safe', supply: 85 },
  { name: 'Mile 6', coords: [5.978, 10.147], status: 'risk', supply: 45 },
  { name: 'Food Market', coords: [5.961, 10.158], status: 'safe', supply: 120 },
  { name: 'Commercial Avenue', coords: [5.958, 10.150], status: 'safe', supply: 95 },
  { name: 'Bambili', coords: [5.988, 10.250], status: 'disrupted', supply: 10 },
];

function App() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isOffline, setIsOffline] = useState(false);

  // Polling logic: fetch every 10 seconds
  useEffect(() => {
    const fetchRecords = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/records');
        if (response.ok) {
          const data = await response.json();
          setRecords(data);
          setIsOffline(false);
        } else {
          setIsOffline(true);
        }
      } catch (error) {
        console.error("Error fetching records:", error);
        setIsOffline(true);
      } finally {
        setLoading(false);
      }
    };

    fetchRecords();
    const interval = setInterval(fetchRecords, 10000);
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'safe': return '#10b981'; // emerald-500
      case 'risk': return '#f59e0b'; // amber-500
      case 'disrupted': return '#ef4444'; // red-500
      default: return '#64748b';
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 font-sans flex flex-col">
      {/* Header */}
      <header className="px-8 py-6 border-b border-slate-800 flex justify-between items-center glass-panel">
        <div>
          <h1 className="text-2xl font-bold text-emerald-500 tracking-tight">HallaMarket <span className="text-slate-400 font-light">| Command Center</span></h1>
          <p className="text-xs text-slate-500 uppercase tracking-widest mt-1">Bamenda Supply Chain Resilience Engine</p>
        </div>
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${isOffline ? 'bg-red-500' : 'bg-emerald-500'} animate-pulse`}></div>
            <span className={`text-sm font-medium ${isOffline ? 'text-red-500' : 'text-emerald-500'}`}>
              {isOffline ? 'Offline Mode' : 'Live Network Active'}
            </span>
          </div>
          <div className="text-right">
            <p className="text-xs text-slate-500">Total Records</p>
            <p className="text-lg font-bold leading-none">{records.length || '---'}</p>
          </div>
        </div>
      </header>

      {/* Offline Notification Bar */}
      {isOffline && (
        <div className="bg-amber-600/20 border-b border-amber-600/30 px-8 py-2 flex items-center justify-between">
          <div className="flex items-center gap-2 text-amber-500 text-xs font-bold uppercase tracking-wider">
            <AlertTriangle size={14} />
            Offline Data-Caching State: Connection to backend lost. Displaying cached data.
          </div>
          <button 
            onClick={() => window.location.reload()} 
            className="text-[10px] bg-amber-600/40 hover:bg-amber-600/60 text-white px-3 py-1 rounded transition-colors"
          >
            RECONNECT
          </button>
        </div>
      )}

      <main className="flex-1 flex overflow-hidden">
        {/* Left Sidebar: Transcriptions */}
        <aside className="w-96 border-r border-slate-800 flex flex-col bg-slate-900/50">
          <div className="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-800/30">
            <h2 className="text-sm font-semibold uppercase text-slate-400 flex items-center gap-2">
              <MessageSquare size={16} className="text-emerald-500" />
              Incoming Pipeline
            </h2>
            <span className="text-[10px] bg-slate-700 px-2 py-0.5 rounded text-slate-300">AUTO-SYNC ON</span>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {records.length === 0 ? (
              <div className="text-center py-12 opacity-30 italic text-sm">Waiting for incoming logs...</div>
            ) : (
              records.map((rec, i) => (
                <div key={rec.id || i} className="p-4 rounded-xl border border-slate-800 bg-slate-800/40 hover:border-emerald-500/50 transition-colors group">
                  <div className="flex justify-between items-start mb-2">
                    <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase ${rec.source === 'whatsapp' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-blue-500/10 text-blue-500'}`}>
                      {rec.source}
                    </span>
                    <span className="text-[10px] text-slate-500 flex items-center gap-1">
                      <Clock size={10} />
                      {new Date(rec.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                  <div className="text-sm font-medium mb-1">{rec.crop || 'Unknown Product'}</div>
                  <div className="text-xs text-slate-400 mb-3 flex items-center gap-1">
                    <MapPin size={12} className="text-slate-500" /> {rec.location || 'Unknown Location'} • {rec.quantity || 'Qty N/A'}
                  </div>
                  <div className="pt-2 border-t border-slate-700/50 flex justify-between items-center">
                    <span className="text-[10px] text-slate-500 italic">Intent: {rec.intent || 'unclassified'}</span>
                    <Activity size={14} className="text-emerald-500/40" />
                  </div>
                </div>
              ))
            )}
          </div>
        </aside>

        {/* Center: Map Canvas */}
        <section className="flex-1 p-6 relative">
          <div className="absolute top-10 right-10 z-[1000] flex flex-col gap-2">
            <div className="glass-panel p-3 rounded-lg border border-slate-700 shadow-2xl">
              <h3 className="text-xs font-bold uppercase text-slate-500 mb-2 tracking-tighter">Corridor Status</h3>
              <div className="space-y-2">
                <StatusItem color="bg-emerald-500" label="Active Supply" />
                <StatusItem color="bg-amber-500" label="High Risk / Unverified" />
                <StatusItem color="bg-red-500" label="Disrupted Corridor" />
              </div>
            </div>
          </div>

          <div className="w-full h-full rounded-2xl overflow-hidden border border-slate-800 shadow-inner">
            <MapContainer center={[5.961, 10.158]} zoom={11} scrollWheelZoom={true}>
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
              />
              {HUBS.map((hub) => (
                <React.Fragment key={hub.name}>
                  <Marker position={hub.coords}>
                    <Popup>
                      <div className="text-slate-900 font-sans">
                        <strong className="text-lg">{hub.name}</strong><br />
                        <span className="text-sm opacity-70">Supply Index: {hub.supply}</span>
                      </div>
                    </Popup>
                  </Marker>
                  <Circle 
                    center={hub.coords} 
                    radius={1500} 
                    pathOptions={{ 
                      fillColor: getStatusColor(hub.status), 
                      color: getStatusColor(hub.status),
                      fillOpacity: 0.2
                    }} 
                  />
                </React.Fragment>
              ))}
            </MapContainer>
          </div>
        </section>
      </main>

      {/* Footer / Crisis Ticker */}
      <footer className="h-10 bg-slate-800 border-t border-slate-700 flex items-center px-4 overflow-hidden">
        <div className="flex items-center gap-2 text-[10px] font-bold text-red-400 uppercase whitespace-nowrap animate-pulse mr-8">
          <AlertTriangle size={14} />
          Crisis Alert:
        </div>
        <div className="text-[10px] text-slate-400 uppercase tracking-widest flex gap-12 animate-marquee">
          <span>Logistics disruption detected on Santa-Bamenda corridor</span>
          <span>Bambili market reporting low stock for Habanero Peppers</span>
          <span>Mile 6 Market weather: Heavy rains may affect transport</span>
          <span>Food Market supply surplus: Irish Potatoes price drop expected</span>
        </div>
      </footer>
    </div>
  );
}

function StatusItem({ color, label }) {
  return (
    <div className="flex items-center gap-2">
      <div className={`w-2 h-2 rounded-full ${color}`}></div>
      <span className="text-[10px] font-medium text-slate-300">{label}</span>
    </div>
  );
}

export default App;
