<template>
  <AppLayout>
    <template #default>
      <div class="space-y-6">
@@
-  async function runAction(a: QuickAction) {
-    // For now, show an alert — in a real app we'd call an endpoint
-    alert(`Running action: ${a.name}`)
-  }
+  const actionMessage = ref('')
+
+  async function runAction(a: QuickAction) {
+    actionMessage.value = `Running action: ${a.name}...`
+    try {
+      // In future we will call the real endpoint: dashboardService.runQuickAction(a.id)
+      setTimeout(() => {
+        actionMessage.value = `Action "${a.name}" executed (mock).`
+      }, 600)
+    } catch (e: any) {
+      actionMessage.value = e?.message || 'Action failed'
+    }
+  }
 </script>
