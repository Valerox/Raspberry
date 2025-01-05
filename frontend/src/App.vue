<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from 'axios';

// Daten für das System speichern
const systemInfo = ref<any | null>(null);
const renderPage = ref(false)

// Daten beim Laden der Komponente abrufen
setInterval(async () => {
  axios.get('http://localhost:5000/system')
  .then(response => {
    systemInfo.value = response.data
    renderPage.value = true
  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });
}, 1000);

// Berechnung für den Memory Progress
const memoryProgress = () => {
  if (!systemInfo.value) return 0;
  return (
    (systemInfo.value.storage_used / systemInfo.value.storage_total) *
    100
  );
};
</script>

<template>
  <main class="min-h-screen bg-background flex flex-col items-center justify-center p-6" v-if="renderPage">
    <h1 class="text-3xl font-bold mb-6">Raspberry Pi</h1>

    <!-- Card für die Systeminformationen -->
    <div class="w-full max-w-md bg-card p-4 rounded-lg shadow-md">
      <header class="border-b pb-2 mb-4">
        <h2 class="text-lg font-semibold text-foreground">System Information</h2>
      </header>
      <section class="space-y-4">
        <!-- Allgemeine Systeminformationen -->
        <div class="space-y-2">
          <div v-for="(value) in [
            ['Hostname', systemInfo?.hostname],
            ['Platform', systemInfo?.platform],
            ['Architecture', systemInfo?.architecture],
            ['CPU Temperature', `${systemInfo?.cpu_temperature?.toFixed(1)}°C`]
          ]" :key="value[0]" class="flex justify-between text-sm">
            <span class="text-muted-foreground">{{ value[0] }}:</span>
            <span class="text-foreground font-medium">{{ value[1] }}</span>
          </div>
        </div>

        <!-- CPU-Auslastung -->
        <div class="space-y-2">
          <h3 class="text-lg font-semibold text-foreground">CPU Usage</h3>
          <div v-for="(usage, index) in systemInfo?.cpu_usage || []" :key="index" class="space-y-1">
            <div class="flex justify-between text-sm text-muted-foreground">
              <span>Core {{ index }}</span>
              <span>{{ usage }}%</span>
            </div>
            <div class="h-2 w-full bg-muted-foreground rounded">
              <div class="bg-foreground h-full rounded" :style="{ width: usage + '%' }"></div>
            </div>
          </div>
        </div>

        <!-- Memory-Auslastung -->
        <div class="space-y-2">
          <h3 class="text-lg font-semibold text-foreground">Memory Usage</h3>
          <div class="flex justify-between text-sm text-muted-foreground">
            <span>Used</span>
            <span>
              {{
                systemInfo?.storage_used.toFixed(2) || 0
              }} / {{
                systemInfo?.storage_total.toFixed(2) || 0
              }} GB
            </span>
          </div>
          <div class="h-2 w-full bg-muted-foreground rounded">
            <div class="bg-foreground h-full rounded" :style="{ width: memoryProgress() + '%' }"></div>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped>
/* Beispielhafte Tailwind-Klassen – passe sie an deinen Bedarf an */

.bg-card {
  background-color: #ffffff;
}

.text-foreground {
  color: #333333;
}

.text-muted-foreground {
  color: #777777;
}

.bg-muted-foreground {
  background-color: #e0e0e0;
}

.bg-foreground {
  background-color: #4caf50;
}
</style>