<template>
  <div class="app">
    <template v-if="authStore.isAuthenticated">
      <Topbar />
      <TimetrackerBar />
    </template>
    <main style="margin-top: 10px;">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRoadmapStore } from '@/stores/roadmap'
import { useTimetrackerStore } from '@/stores/timetracker'
import Topbar from '@/components/Topbar.vue'
import TimetrackerBar from '@/components/TimetrackerBar.vue'

const authStore = useAuthStore()
const roadmapStore = useRoadmapStore()
const timetrackerStore = useTimetrackerStore()

onMounted(async () => {
  if (authStore.isAuthenticated) {
    if (authStore.user?.id) {
      timetrackerStore.initFromStorage(authStore.user.id)
    } else {
      await authStore.fetchMe()
    }
    await Promise.all([
      roadmapStore.fetchAll(),
      timetrackerStore.fetchMyEntries()
    ])
  } else {
    timetrackerStore.clearSessionTimer()
  }
})
</script>

