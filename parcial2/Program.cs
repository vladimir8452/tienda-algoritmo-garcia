// vladimir Garcia Rojas

using System.Diagnostics;
using System.Globalization;

namespace Parcial2.VarianteB;

public interface IReceptorPedidos
{
    void Registrar(string pedido, int plazoMinutos);   // llega un pedido (nombres únicos)
    string? PrepararSiguiente();                       // saca y devuelve el de menor plazo; null si no hay ninguno
    bool EstaPendiente(string pedido);                 // ¿este pedido sigue pendiente? (prepararlo lo saca)
    int Pendientes { get; }                            // cuántos hay pendientes
}

public sealed record Pedido(string Nombre, int Plazo, int Llegada);

// ---------- SOLUCIÓN INGENUA (lista simple): correcta pero lenta ----------
public sealed class ReceptorIngenuo : IReceptorPedidos
{
    private readonly List<Pedido> _lista = new();
    private int _llegadas;

    public void Registrar(string pedido, int plazoMinutos) => _lista.Add(new Pedido(pedido, plazoMinutos, _llegadas++));

    public string? PrepararSiguiente()
    {
        if (_lista.Count == 0) return null;
        int mejor = 0;
        for (int i = 1; i < _lista.Count; i++)
        {
            var p = _lista[i]; var m = _lista[mejor];
            if (p.Plazo < m.Plazo || (p.Plazo == m.Plazo && p.Llegada < m.Llegada)) mejor = i;
        }
        string nombre = _lista[mejor].Nombre;
        _lista.RemoveAt(mejor);
        return nombre;
    }

    public bool EstaPendiente(string pedido)
    {
        foreach (var p in _lista) if (p.Nombre == pedido) return true;
        return false;
    }

    public int Pendientes => _lista.Count;
}

// ---------- MI SOLUCIÓN: montículo mínimo + conjunto hash ----------
public sealed class ReceptorMejorado : IReceptorPedidos
{
    // Montículo mínimo: en la raíz queda el pedido más urgente.
    // La prioridad es (plazo, llegada): menor plazo primero y, si empatan, el que llegó antes.
    // Las tuplas se comparan elemento por elemento, primero Plazo y luego Llegada.
    private readonly PriorityQueue<string, (int Plazo, int Llegada)> _cola = new();

    // Nombres de los pedidos pendientes: responde EstaPendiente sin recorrer nada.
    private readonly HashSet<string> _pendientes = new();

    private int _llegadas;

    // O(log n) (montículo) + O(1) promedio (conjunto)
    public void Registrar(string pedido, int plazoMinutos)
    {
        _cola.Enqueue(pedido, (plazoMinutos, _llegadas++));
        _pendientes.Add(pedido);
    }

    // O(log n): saca la raíz del montículo y quita el nombre del conjunto
    public string? PrepararSiguiente()
    {
        if (!_cola.TryDequeue(out var nombre, out _)) return null;
        _pendientes.Remove(nombre);
        return nombre;
    }

    // O(1) promedio
    public bool EstaPendiente(string pedido) => _pendientes.Contains(pedido);

    // O(1)
    public int Pendientes => _pendientes.Count;
}

public static class Programa
{
    // El guion de pruebas: cada paso es (operación, argumento, plazo, resultado esperado).
    private static readonly (string op, string arg, int plazo, string esperado)[] Guion =
    {
        ("registrar", "Torta", 120, ""), ("registrar", "Galletas", 30, ""), ("registrar", "Pan", 120, ""), ("registrar", "Brazo", 60, ""),
        ("pendientes", "", 0, "4"),
        ("esta", "Galletas", 0, "True"), ("esta", "Flan", 0, "False"),
        ("preparar", "", 0, "Galletas"), ("esta", "Galletas", 0, "False"),
        ("preparar", "", 0, "Brazo"),
        ("registrar", "Alfajor", 30, ""),
        ("preparar", "", 0, "Alfajor"), ("preparar", "", 0, "Torta"), ("preparar", "", 0, "Pan"),
        ("preparar", "", 0, "(ninguno)"), ("pendientes", "", 0, "0"),
    };

    private static string Ejecutar(IReceptorPedidos g, string op, string arg, int plazo)
    {
        switch (op)
        {
            case "registrar": g.Registrar(arg, plazo); return "";
            case "preparar": return g.PrepararSiguiente() ?? "(ninguno)";
            case "esta": return g.EstaPendiente(arg).ToString();
            default: return g.Pendientes.ToString();
        }
    }

    private static void Probar(string titulo, IReceptorPedidos g)
    {
        int bien = 0, total = 0;
        try
        {
            foreach (var (op, arg, plazo, esperado) in Guion)
            {
                string obtenido = Ejecutar(g, op, arg, plazo);
                if (op == "registrar") continue;
                total++;
                if (obtenido == esperado) bien++;
                else Console.WriteLine($"   MAL en «{op} {arg}»: esperado {esperado}, obtuvo {obtenido}");
            }
            Console.WriteLine($"{titulo}: {bien} de {total} pasos correctos");
        }
        catch (NotImplementedException) { Console.WriteLine($"{titulo}: (sin escribir todavía)"); }
    }

    // La CARGA para medir: n pedidos llegan y después se preparan los n.
    public static long EjecutarCarga(IReceptorPedidos g, int n)
    {
        for (int i = 0; i < n; i++) g.Registrar("Q" + i, ((int)((i * 6007L) % 6) + 1) * 15);
        long control = 0;
        for (int i = 0; i < n; i++) control += g.PrepararSiguiente()!.Length;
        return control;
    }

    private const int N = 10_000;         // tamaños que se miden: N, 2N y 4N
    private const int Repeticiones = 3;   // corridas medidas (más 1 de calentamiento)
    private static long _control;         // evita que el compilador descarte la carga

    // Protocolo: 1 corrida de calentamiento (no se mide) + 3 corridas medidas.
    // Cada corrida usa un receptor nuevo y vacío; crearlo no entra en el tiempo medido.
    private static double[] Medir(Func<IReceptorPedidos> crear, int n)
    {
        _control += EjecutarCarga(crear(), n);   // calentamiento

        var tiempos = new double[Repeticiones];
        for (int r = 0; r < Repeticiones; r++)
        {
            var receptor = crear();
            var reloj = Stopwatch.StartNew();
            _control += EjecutarCarga(receptor, n);
            reloj.Stop();
            tiempos[r] = reloj.Elapsed.TotalMilliseconds;
        }
        return tiempos;
    }

    // Dispersión relativa entre las corridas: (máximo - mínimo) / promedio, en %.
    private static double Ruido(double[] t) => (t.Max() - t.Min()) / t.Average() * 100;

    private static string Num(double x, string formato) => x.ToString(formato, CultureInfo.InvariantCulture);

    public static void Main()
    {
        Probar("ReceptorIngenuo ", new ReceptorIngenuo());
        Probar("ReceptorMejorado", new ReceptorMejorado());
        Console.WriteLine();

        Console.WriteLine($"Protocolo: 1 calentamiento + {Repeticiones} corridas medidas, promedio | n = {N}, {2 * N}, {4 * N}");
        Console.WriteLine();

        var filas = new List<(int n, double[] ing, double[] mej)>();
        foreach (int tam in new[] { N, 2 * N, 4 * N })
        {
            var ing = Medir(() => new ReceptorIngenuo(), tam);
            var mej = Medir(() => new ReceptorMejorado(), tam);
            filas.Add((tam, ing, mej));
        }

        Console.WriteLine("| n | Ingenua: ms (promedio) | Ingenua: veces vs fila anterior | Ingenua: ruido | Mejorada: ms (promedio) | Mejorada: veces vs fila anterior | Mejorada: ruido |");
        Console.WriteLine("|---|---|---|---|---|---|---|");
        double? antIng = null, antMej = null;
        foreach (var fila in filas)
        {
            double pi = fila.ing.Average(), pm = fila.mej.Average();
            string vi = antIng is null ? "—" : Num(pi / antIng.Value, "F2");
            string vm = antMej is null ? "—" : Num(pm / antMej.Value, "F2");
            antIng = pi; antMej = pm;
            string n = Num(fila.n, "N0");
            Console.WriteLine($"| {n} | {Num(pi, "F2")} | {vi} | {Num(Ruido(fila.ing), "F0")} % | {Num(pm, "F3")} | {vm} | {Num(Ruido(fila.mej), "F0")} % |");
        }

        Console.WriteLine();
        Console.WriteLine("Las 3 corridas medidas de cada celda (ms):");
        Console.WriteLine("| n | Ingenua | Mejorada |");
        Console.WriteLine("|---|---|---|");
        foreach (var fila in filas)
        {
            string n = Num(fila.n, "N0");
            string ing = string.Join(" / ", fila.ing.Select(t => Num(t, "F2")));
            string mej = string.Join(" / ", fila.mej.Select(t => Num(t, "F3")));
            Console.WriteLine($"| {n} | {ing} | {mej} |");
        }

        double mayor = filas[^1].ing.Average();
        Console.WriteLine();
        if (mayor < 500 || mayor > 20_000)
            Console.WriteLine($"AVISO: la ingenua con {4 * N} tardó {Num(mayor, "F0")} ms y debe estar entre 500 y 20000 ms. Cambia N (constante al inicio de Programa) y vuelve a ejecutar.");
        else
            Console.WriteLine($"La ingenua con {4 * N} tardó {Num(mayor, "F0")} ms: dentro del rango pedido (500 a 20000 ms).");
        Console.WriteLine($"(control: {_control})");
    }
}
