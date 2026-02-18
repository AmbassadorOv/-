/*
Provenance header: keep this block in every generated artifact.
*/

import React, { useState, useEffect } from 'react';
import governor from './governor-module';

/**
 * Main Dashboard Component for Project Lamina.
 *
 * Features a "Truth Gauge" that validates all incoming data through the Ontological Kernel.
 */
const MainDashboard = ({ dataStream }) => {
    const [isTruthValidated, setIsTruthValidated] = useState(false);
    const [truthGaugeText, setTruthGaugeText] = useState("Awaiting Logic...");
    const [safeData, setSafeData] = useState(null);
    const [ontologicalNoise, setOntologicalNoise] = useState(false);

    useEffect(() => {
        if (dataStream) {
            try {
                // Each datum must pass through kernel.validate_logic via the Governor.
                const validated = governor.validate(dataStream);
                setSafeData(validated);
                setIsTruthValidated(true);
                setTruthGaugeText("💎 441 Validated");
                setOntologicalNoise(false);
            } catch (error) {
                // If the combination is not in the 231 gates -> block output.
                setIsTruthValidated(false);
                setTruthGaugeText("⚠️ Hallucination Warning");
                setSafeData(null);
                setOntologicalNoise(true);
            }
        }
    }, [dataStream]);

    return (
        <div style={{ padding: '20px', backgroundColor: '#121212', color: '#e0e0e0', fontFamily: 'monospace' }}>
            <h1 style={{ borderBottom: '1px solid #333' }}>PROJECT LAMINA - Governor Module</h1>

            {/* Truth Gauge Indicator */}
            <div style={{
                margin: '20px 0',
                padding: '15px',
                border: '2px solid',
                borderColor: isTruthValidated ? '#00ff00' : '#ff0000',
                borderRadius: '8px',
                textAlign: 'center',
                fontSize: '1.5em'
            }}>
                Truth Gauge: <strong>{truthGaugeText}</strong>
            </div>

            <div style={{ marginTop: '30px' }}>
                <h3>Kernel Output:</h3>
                <div style={{
                    backgroundColor: '#000',
                    padding: '15px',
                    borderRadius: '5px',
                    minHeight: '100px',
                    border: '1px solid #444'
                }}>
                    {ontologicalNoise ? (
                        <div style={{ color: '#ff5555', fontWeight: 'bold' }}>
                            [!] Ontological Noise Detected. Output blocked.
                        </div>
                    ) : (
                        <pre>{safeData ? JSON.stringify(safeData, null, 2) : "System Standby..."}</pre>
                    )}
                </div>
            </div>

            <div style={{ marginTop: '40px', fontSize: '0.8em', color: '#666' }}>
                <p>PROJECT LAMINA - PROTECTED BY NON-PROFIT ENTITY (חל"צ). CORE KERNEL IS NON-COMMERCIAL.</p>
            </div>
        </div>
    );
};

export default MainDashboard;
