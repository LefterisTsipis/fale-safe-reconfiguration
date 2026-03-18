// Endpoint URL (replace with your actual endpoint)
const endpoint = 'http://localhost:8000/sdn_app/api/topology/info'; // Change this URL to your actual endpoint

// Fetch JSON data from the endpoint
fetch(endpoint)
    .then(response => response.json())
    .then(data => {
        const hostMacInfo = data.data.host_mac_info;
        const hostSwitchMapping = data.data.host_switch_mapping;
        const hostPortMapping = data.data.host_port_mapping_to_switch;

        // Get the table body element
        const tableBody = document.getElementById('table-body');

        // Loop through the host_mac_info object and add rows to the table
        for (const host in hostMacInfo) {
            if (hostMacInfo.hasOwnProperty(host)) {
                const macAddress = hostMacInfo[host];
                const switchMapping = hostSwitchMapping[host];
                const portMapping = hostPortMapping[host];

                // Create a new row
                const row = document.createElement('tr');

                // Create cells for each piece of data
                const hostCell = document.createElement('td');
                const macCell = document.createElement('td');
                const switchCell = document.createElement('td');
                const portCell = document.createElement('td');

                // Fill the cells with data
                hostCell.textContent = host;
                macCell.textContent = macAddress;
                switchCell.textContent = switchMapping;
                portCell.textContent = portMapping;

                // Append cells to the row
                row.appendChild(hostCell);
                row.appendChild(macCell);
                row.appendChild(switchCell);
                row.appendChild(portCell);

                // Append the row to the table body
                tableBody.appendChild(row);
            }
        }
    })
    .catch(error => console.error('Error fetching JSON data:', error));
