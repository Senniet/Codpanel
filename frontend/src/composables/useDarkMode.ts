export function useDark() {
  const isDark = ref(document.documentElement.classList.contains('dark'))

  function setDark(v: boolean) {
    isDark.value = v
    document.documentElement.classList.toggle('dark', v)
    try { localStorage.setItem('codpanel:dark', v ? '1' : '0') } catch (e) {}
  }

  function toggle() { setDark(!isDark.value) }

  // init
  try {
    const saved = localStorage.getItem('codpanel:dark')
    if (saved !== null) setDark(saved === '1')
    else {
      // respect prefers-color-scheme
      const prefers = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
      setDark(prefers)
    }
  } catch (e) {
    // ignore
  }

  return { isDark, setDark, toggle }
}
