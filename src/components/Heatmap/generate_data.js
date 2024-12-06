function generateRandomIPData(sourceIPs, destinationIPs, minValue, maxValue) {
    const data = [];
    
    // Loop through each source IP (group)
    sourceIPs.forEach(sourceIp => {
        // Loop through each destination IP (variable)
        destinationIPs.forEach(destinationIp => {
            // Generate a random frequency
            const frequency = Math.random() < 0.9 // 90% chance to assign a random value
                ? Math.floor(Math.random() * (maxValue - minValue + 1)) + minValue
                : 0; // 10% chance to assign 0

            // Add the row to the data array
            data.push({ sourceIp, destinationIp, frequency });
        });
    });

    return data;
}

// Helper function to generate random IP addresses
function generateRandomIP() {
    return `${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}`;
}

export default function generateMockData() {
    // Example usage:
    const sourceIPs = Array.from({ length: 50}, generateRandomIP); // Generate 5 random source IPs
    const destinationIPs = Array.from({ length: 50}, generateRandomIP); // Generate 5 random source IPs
    //const destinationIPs = Array.from({ length: 2}, generateRandomIP); // Generate 5 random destination IPs
    const minValue = 0; // Minimum frequency
    const maxValue = 100; // Maximum frequency

    const generatedData = generateRandomIPData(sourceIPs, destinationIPs, minValue, maxValue);

    // Return the generated data as a list of objects
    return generatedData;
}